import os
from pathlib import Path
import re
from typing import List, Dict, Optional


class DirectoryIndexer:
    def __init__(self, root_path: str, ignore_patterns: Optional[List[str]] = None):
        self.root_path = Path(root_path)
        self.ignore_patterns = ignore_patterns or ['.git', '__pycache__', '.ipynb_checkpoints', 'venv', 'env']
        self.chapter_counter = 1

    def should_ignore(self, path: Path) -> bool:
        return any(pattern in str(path) for pattern in self.ignore_patterns)

    def clean_name(self, name: str) -> str:
        name = os.path.splitext(name)[0]
        name = name.replace('_', ' ').replace('-', ' ')
        name = re.sub('([a-z])([A-Z])', r'\1 \2', name)
        return ' '.join(word.capitalize() for word in name.split())

    def create_markdown_link(self, name: str, path: Path) -> str:
        """Create a markdown link with the relative path."""
        clean_title = self.clean_name(name)
        # Create filename from the clean title
        filename = clean_title.lower().replace(' ', '_') + '.md'
        # Get relative path from root
        rel_path = os.path.relpath(path, self.root_path)
        # Replace backslashes with forward slashes for consistency
        rel_path = rel_path.replace('\\', '/')
        return f"- [{clean_title}]({rel_path}/{filename})"

    def get_directory_structure(self) -> Dict:
        def recurse(current_path: Path, depth: int = 0) -> Dict:
            if self.should_ignore(current_path):
                return None

            result = {
                'name': current_path.name,
                'path': current_path,
                'depth': depth,
                'children': []
            }

            try:
                for path in sorted(current_path.iterdir()):
                    if path.is_dir() and not self.should_ignore(path):
                        child_result = recurse(path, depth + 1)
                        if child_result:
                            result['children'].append(child_result)
            except PermissionError:
                pass

            return result

        return recurse(self.root_path)

    def generate_markdown(self, structure: Dict = None, level: int = 1) -> str:
        if structure is None:
            structure = self.get_directory_structure()

        markdown_lines = []

        # Add title only for root level
        if level == 1:
            markdown_lines.extend([
                "# Directory Index\n",
                f"Generated from: {self.root_path}\n",
                "---\n"
            ])

        # Add current directory as a link if not root
        if level > 1:
            markdown_link = self.create_markdown_link(structure['name'], structure['path'])
            markdown_lines.append(markdown_link)

        # Process children with indentation
        if structure['children']:
            for child in structure['children']:
                child_content = self.generate_markdown(child, level + 1)
                # Add indentation for children
                indented_content = '\n'.join('  ' * (level - 1) + line
                                             for line in child_content.split('\n') if line)
                markdown_lines.append(indented_content)

        return '\n'.join(markdown_lines)

    def create_index(self, output_file: Optional[str] = None) -> str:
        markdown_content = self.generate_markdown()

        if output_file:
            output_path = Path(output_file)
            output_path.write_text(markdown_content)
            print(f"Index saved to: {output_path.absolute()}")

        return markdown_content


# Example usage
if __name__ == "__main__":
    indexer = DirectoryIndexer("src",
                               ignore_patterns=[".idea",".git","venv"])
    markdown_content = indexer.create_index("index.md")
    print("Index generated successfully!")