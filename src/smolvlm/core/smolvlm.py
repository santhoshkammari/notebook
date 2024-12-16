import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM
from typing import List, Optional, Tuple, Dict


class VisionEncoder(nn.Module):
    def __init__(
        self,
        image_size: int = 384,
        patch_size: int = 14,
        hidden_size: int = 768,
        num_attention_heads: int = 12,
        num_encoder_layers: int = 12
    ):
        super().__init__()
        # SigLIP-based vision encoder
        self.patch_embed = nn.Conv2d(3, hidden_size, kernel_size=patch_size, stride=patch_size)
        self.pos_embed = nn.Parameter(torch.zeros(1, (image_size // patch_size) ** 2, hidden_size))

        # Transformer encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=num_attention_heads,
            dim_feedforward=hidden_size * 4,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_encoder_layers)

        # Pixel shuffle compression (9x)
        self.compression = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 9),
            nn.LayerNorm(hidden_size // 9)
        )

    def forward(self, pixel_values: torch.Tensor) -> torch.Tensor:
        # Shape: [batch_size, channels, height, width] -> [batch_size, num_patches, hidden_size]
        x = self.patch_embed(pixel_values)
        x = x.flatten(2).transpose(1, 2)

        # Add positional embeddings
        x = x + self.pos_embed

        # Apply transformer layers
        x = self.encoder(x)

        # Compress features
        x = self.compression(x)
        return x


class ModalityProjection(nn.Module):
    def __init__(self, hidden_size: int = 768, compressed_size: int = 85):
        super().__init__()
        self.visual_projection = nn.Linear(compressed_size, hidden_size)
        self.pooling = nn.MultiheadAttention(hidden_size, 8, batch_first=True)
        self.layer_norm = nn.LayerNorm(hidden_size)

    def forward(
        self,
        visual_features: torch.Tensor,
        text_features: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        # Project visual features to language space
        visual_projected = self.visual_projection(visual_features)

        if text_features is not None:
            # Cross-attention pooling between visual and text features
            pooled_features, _ = self.pooling(
                text_features,
                visual_projected,
                visual_projected
            )
            return self.layer_norm(pooled_features + text_features)

        return self.layer_norm(visual_projected)


class SmolVLM(nn.Module):
    def __init__(
        self,
        vision_encoder: VisionEncoder,
        modality_projection: ModalityProjection,
        language_model: AutoModelForCausalLM,
        max_position_embeddings: int = 16384
    ):
        super().__init__()
        self.vision_encoder = vision_encoder
        self.modality_projection = modality_projection
        self.language_model = language_model

        # Extended position embeddings for long context
        self.rope_scaling = {"factor": 27.3}  # 273k/10k as per paper

    def preprocess_images(
        self,
        pixel_values: torch.Tensor,
        image_sizes: List[Tuple[int, int]]
    ) -> torch.Tensor:
        # Resize images to 384x384
        processed_images = F.interpolate(
            pixel_values,
            size=(384, 384),
            mode='bilinear',
            align_corners=False
        )
        return processed_images

    def forward(
        self,
        pixel_values: Optional[torch.Tensor] = None,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        image_sizes: Optional[List[Tuple[int, int]]] = None,
        return_dict: bool = True
    ) -> Dict[str, torch.Tensor]:
        batch_size = input_ids.shape[0] if input_ids is not None else pixel_values.shape[0]

        # Process images if provided
        if pixel_values is not None:
            processed_images = self.preprocess_images(pixel_values, image_sizes)
            visual_features = self.vision_encoder(processed_images)
        else:
            visual_features = None

        # Get language model hidden states
        language_outputs = self.language_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            output_hidden_states=True,
            return_dict=True
        )
        text_features = language_outputs.hidden_states[-1]

        # Combine visual and text features
        if visual_features is not None:
            combined_features = self.modality_projection(
                visual_features=visual_features,
                text_features=text_features
            )
        else:
            combined_features = text_features

        # Language model prediction
        lm_logits = self.language_model.lm_head(combined_features)

        # Calculate loss if labels provided
        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(lm_logits.view(-1, lm_logits.size(-1)), labels.view(-1))

        return {
            "loss": loss,
            "logits": lm_logits,
            "hidden_states": combined_features
        } if return_dict else (loss, lm_logits, combined_features)


# Example usage
def create_smolvlm_model(pretrained_lm_path: str = "HuggingFaceTB/SmolLM2"):
    vision_encoder = VisionEncoder()
    modality_projection = ModalityProjection()
    language_model = AutoModelForCausalLM.from_pretrained(
        pretrained_lm_path,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True
    )

    model = SmolVLM(
        vision_encoder=vision_encoder,
        modality_projection=modality_projection,
        language_model=language_model
    )
    return model