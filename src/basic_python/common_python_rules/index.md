# Python Best Practices and Guidelines

A comprehensive guide to writing clean, maintainable, and scalable Python code.

## Table of Contents
- [Core Principles](#core-principles)
- [Code Organization](#code-organization)
- [Type Hints and Data Classes](#type-hints-and-data-classes)
- [Error Handling](#error-handling)
- [Design Patterns](#design-patterns)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Common Anti-patterns to Avoid](#common-anti-patterns-to-avoid)

## Core Principles

### 1. Use Type Hints
Always use type hints for better code readability and IDE support.

```python
# ❌ Bad
def process_user(name, age, preferences):
    return {"name": name.strip(), "age": age, "settings": preferences}

# ✅ Good
from typing import Dict, Any

def process_user(name: str, age: int, preferences: Dict[str, Any]) -> Dict[str, Any]:
    return {"name": name.strip(), "age": age, "settings": preferences}
```

### 2. Use Dataclasses
Use dataclasses for structured data instead of plain classes.

```python
# ❌ Bad
class UserConfig:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.preferences = {}

# ✅ Good
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class UserConfig:
    name: str = ""
    age: int = 0
    preferences: Dict[str, Any] = field(default_factory=dict)
```

## Code Organization

### 1. Project Structure
```
project/
├── config/
│   ├── __init__.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── models.py
│   └── interfaces.py
├── services/
│   ├── __init__.py
│   └── processor.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── tests/
    ├── __init__.py
    └── test_processor.py
```

### 2. Interface Definitions
Use abstract base classes or protocols for interfaces.

```python
from abc import ABC, abstractmethod
from typing import Protocol

# Using ABC
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: bytes) -> str:
        pass

# Using Protocol
class MessageHandler(Protocol):
    def handle(self, message: str) -> None: ...
```

## Type Hints and Data Classes

### 1. Complex Type Hints
```python
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

class Repository(Generic[T]):
    def get(self, id: str) -> Optional[T]:
        ...
    
    def save(self, item: T) -> None:
        ...

    def get_all(self) -> List[T]:
        ...
```

### 2. Advanced Dataclass Usage
```python
@dataclass
class Configuration:
    debug: bool = field(default=False)
    timeout: int = field(default=30)
    retries: int = field(default=3)
    
    def __post_init__(self):
        if self.retries < 0:
            raise ValueError("Retries cannot be negative")
```

## Error Handling

### 1. Custom Exceptions
```python
class ServiceError(Exception):
    """Base exception for service errors."""
    pass

class ValidationError(ServiceError):
    """Raised when data validation fails."""
    pass

class ProcessingError(ServiceError):
    """Raised when data processing fails."""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error
```

### 2. Proper Error Handling
```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_configuration(path: Path) -> Dict[str, Any]:
    try:
        with path.open() as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {path}")
        raise ConfigurationError(f"Missing configuration file: {path}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration: {e}")
        raise ConfigurationError(f"Invalid configuration format: {e}")
```

## Design Patterns

### 1. Factory Pattern
```python
class ProcessorFactory:
    @staticmethod
    def create(type_: str) -> Processor:
        match type_:
            case "text":
                return TextProcessor()
            case "binary":
                return BinaryProcessor()
            case _:
                raise ValueError(f"Unknown processor type: {type_}")
```

### 2. Dependency Injection
```python
class MessageService:
    def __init__(
        self,
        processor: MessageProcessor,
        validator: MessageValidator,
        logger: Logger
    ):
        self._processor = processor
        self._validator = validator
        self._logger = logger
```

## Testing Guidelines

### 1. Test Structure
```python
import pytest
from unittest.mock import Mock

class TestMessageProcessor:
    @pytest.fixture
    def processor(self):
        return MessageProcessor()
    
    def test_process_valid_message(self, processor):
        # Arrange
        message = "test message"
        
        # Act
        result = processor.process(message)
        
        # Assert
        assert result.is_valid
        assert result.content == "TEST MESSAGE"
```

### 2. Mock Usage
```python
def test_service_with_mock():
    # Arrange
    mock_repository = Mock()
    mock_repository.get.return_value = {"id": "1", "name": "Test"}
    service = Service(repository=mock_repository)
    
    # Act
    result = service.get_data("1")
    
    # Assert
    assert result["name"] == "Test"
    mock_repository.get.assert_called_once_with("1")
```

## Documentation Standards

### 1. Function Documentation
```python
def calculate_total(
    items: List[Item],
    tax_rate: float = 0.1
) -> float:
    """Calculate total cost including tax.
    
    Args:
        items: List of items to calculate total for
        tax_rate: Tax rate as a decimal (default: 0.1)
    
    Returns:
        Total cost including tax
    
    Raises:
        ValueError: If tax_rate is negative
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

### 2. Class Documentation
```python
class DataProcessor:
    """Processes data according to specified rules.
    
    This class handles the processing of various data formats
    and applies transformation rules.
    
    Attributes:
        rules: List of processing rules to apply
        logger: Logger instance for tracking processing
    """
```

## Common Anti-patterns to Avoid

### 1. Global State
```python
# ❌ Bad
global_config = {}

def update_config():
    global global_config
    global_config['updated'] = True

# ✅ Good
class ConfigManager:
    def __init__(self):
        self._config = {}
    
    def update(self):
        self._config['updated'] = True
```

### 2. Mixed Responsibilities
```python
# ❌ Bad
class UserService:
    def save_user(self):  # Database logic
        pass
    def validate_email(self):  # Validation logic
        pass
    def render_profile(self):  # UI logic
        pass

# ✅ Good
class UserRepository:
    def save_user(self): pass

class UserValidator:
    def validate_email(self): pass

class UserProfileView:
    def render_profile(self): pass
```

## Best Practices Checklist

- [ ] Use type hints consistently
- [ ] Implement proper error handling
- [ ] Write tests for new functionality
- [ ] Document classes and functions
- [ ] Use dependency injection
- [ ] Keep functions and classes focused
- [ ] Avoid global state
- [ ] Use logging effectively
- [ ] Make configuration manageable
- [ ] Plan for future extensions

## References

1. [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
2. [Python Type Hints](https://docs.python.org/3/library/typing.html)
3. [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
4. [Python Testing with pytest](https://docs.pytest.org/en/stable/)