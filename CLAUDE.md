# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
AMEM (Associative Memory for Expectation Maximization) is a Python package implementing the algorithm described in https://arxiv.org/pdf/2502.12110. The package combines associative memory techniques with expectation maximization for improved machine learning performance.

## Development Commands

### Environment Setup
```bash
# Install package in development mode with all dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit -m unit

# Run only integration tests  
pytest tests/integration -m integration

# Run tests with coverage
pytest --cov=amem --cov-report=html

# Run specific test file
pytest tests/unit/test_memory.py -v
```

### Code Quality
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Format code with ruff
ruff format .

# Lint code with ruff
ruff check . --fix

# Type checking with mypy
mypy src/amem

# Run linting and type checking together
ruff check . && mypy src/amem
```

### Building
```bash
# Build package
python -m build

# Install from local build
pip install dist/amem-*.whl
```

## Architecture

### Core Design Principles
- **SOLID Principles**: Especially dependency injection through constructors
- **Interface Segregation**: All core components implement abstract interfaces
- **Dependency Injection**: All dependencies managed through `dependency-injector` library
- **Strict Typing**: Python 3.12+ with mypy strict mode (except short helper functions)

### Package Structure
```
src/amem/
├── __init__.py              # Package entry point
├── container.py             # DI container configuration
├── core/                    # Core algorithm implementations
│   ├── interfaces.py        # Abstract interfaces (IMemoryStore, IExpectationMaximizer, etc.)
│   ├── memory.py           # Associative memory implementation
│   └── em.py               # Expectation maximization implementation
└── services/               # High-level service layer
    └── amem_service.py     # Main AMEM service orchestrating core components
```

### Dependency Injection
- Main container: `amem.container.Container`
- Global instance: `amem.container.container`
- Decorators available: `@inject_memory_store`, `@inject_em`, `@inject_amem_service`
- All dependencies injected through constructors following SOLID principles

### Testing Structure
- Unit tests: `tests/unit/` - Test individual components in isolation
- Integration tests: `tests/integration/` - Test component interactions
- Fixtures in `tests/conftest.py` provide DI containers for testing
- Use `pytest` markers: `@pytest.mark.unit`, `@pytest.mark.integration`

## Development Notes

### Type Hints
- **Mandatory** for all function signatures, class attributes, and variables
- **Exception**: Short nested helper functions can omit type hints
- Use `mypy --strict` for type checking
- Import types properly: `from typing import Protocol, TypeVar, Generic`

### Documentation
- **Google-style docstrings** required for all public functions, classes, and methods
- Enforced by ruff pydocstyle rules
- Example format:
  ```python
  def example_function(param1: str, param2: int = 0) -> bool:
      """Brief description of the function.
      
      Longer description if needed. This can span multiple lines
      and provide detailed information about the function's behavior.
      
      Args:
          param1: Description of the first parameter.
          param2: Description of the second parameter. Defaults to 0.
          
      Returns:
          Description of the return value.
          
      Raises:
          ValueError: Description of when this exception is raised.
      """
  ```

### Dependencies
- Core: `numpy`, `scipy`, `dependency-injector`
- Dev: `pytest`, `pytest-cov`, `mypy`, `ruff`, `pre-commit`
- Python 3.12+ required

### Code Style
- Line length: 88 characters (Black compatible)
- Import sorting: `ruff` with `isort` integration
- Linting: `ruff` with extensive rule set including pydocstyle
- Formatting: `ruff format`
- **Docstrings**: Google format enforced by ruff and pydocstyle

### Pre-commit Hooks
- Trailing whitespace and file fixes
- YAML validation
- Ruff linting and formatting
- MyPy type checking (excludes tests/)
- Unit test execution