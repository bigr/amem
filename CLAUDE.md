# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
AMEM (Associative Memory for Expectation Maximization) is a Python package implementing the algorithm described in https://arxiv.org/pdf/2502.12110. The package combines associative memory techniques with expectation maximization for improved machine learning performance.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment (REQUIRED)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip and install package in development mode
pip install --upgrade pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify installation
python --version  # Should show Python 3.12+
pytest --version
mypy --version
ruff --version
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

#### Modern Typing Conventions (Python 3.12+)
- **Use built-in generics**: `list[str]`, `dict[str, int]`, `tuple[int, ...]` instead of `List[str]`, `Dict[str, int]`, `Tuple[int, ...]`
- **Prefer abstract types for parameters**: 
  - Use `Sequence[T]` instead of `list[T]` for read-only sequences
  - Use `Mapping[K, V]` instead of `dict[K, V]` for read-only mappings
  - Use `MutableSequence[T]`, `MutableMapping[K, V]` when mutation is needed
- **Create type aliases** for complex types:
  ```python
  # Define type aliases at module level
  VectorArray = np.ndarray  # Shape: (n_features,)
  MatrixArray = np.ndarray  # Shape: (n_samples, n_features)
  ParameterDict = dict[str, Any]
  MemoryEntry = tuple[np.ndarray, np.ndarray, float]
  ```
- **Use Protocols and Generics** for rich, structural typing:
  ```python
  from typing import Protocol, TypeVar, Generic
  
  T = TypeVar('T')
  
  class Retrievable(Protocol[T]):
      def retrieve(self, query: VectorArray, k: int = 1) -> list[T]:
          ...
  ```
- **Interface naming**: No `I` prefix - use descriptive names like `MemoryStore`, `Optimizer`
- **Import types properly**: `from typing import Protocol, TypeVar, Generic, Sequence, Mapping`

#### Data Structure Conventions
- **Use dataclasses** for data storage with `@dataclass(frozen=True)` when possible
- **Prefer immutable structures** following functional programming principles
- **Example**:
  ```python
  from dataclasses import dataclass
  
  @dataclass(frozen=True)
  class MemoryEntry:
      key: VectorArray
      value: VectorArray
      similarity: float
  
  @dataclass(frozen=True)
  class ModelParameters:
      means: ComponentMeans
      covariances: ComponentCovariances
      weights: ComponentWeights
      converged: bool
  ```

#### Functional Programming Style
- **Prefer functional patterns** inspired by Haskell
- **Use immutable data structures** when possible
- **Favor composition over inheritance**
- **Use pure functions** without side effects where applicable
- **Example patterns**:
  ```python
  # Pure function composition
  def pipeline[T, U, V](f: Callable[[T], U], g: Callable[[U], V]) -> Callable[[T], V]:
      return lambda x: g(f(x))
  
  # Immutable updates
  def update_parameters(params: ModelParameters, **kwargs) -> ModelParameters:
      return dataclasses.replace(params, **kwargs)
  ```

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
- **Python 3.12+ required**
- Core: `numpy`, `scipy`, `dependency-injector`
- Dev: `pytest`, `pytest-cov`, `mypy`, `ruff`, `pre-commit`

### Development Environment
- **ALWAYS use virtual environment** for development
- Activate virtual environment before any development work
- All commands in this file assume virtual environment is active
- Add `venv/` to `.gitignore` (already included)

### Code Style
- Line length: 88 characters (Black compatible)
- Import sorting: `ruff` with `isort` integration
- Linting: `ruff` with extensive rule set including pydocstyle
- Formatting: `ruff format`
- **Docstrings**: Google format enforced by ruff and pydocstyle

### Commit and Pull Request Conventions

#### Commit Guidelines
- **Atomic commits**: Each commit should be a single logical change
- **Include tests**: Every commit with implementation should include corresponding unit tests
- **Tests must pass**: All tests must pass on every commit
- **Use gitmoji**: Prefix commit messages with appropriate emoji
  - 🎉 `:tada:` - Initial commit
  - ✨ `:sparkles:` - New feature
  - 🐛 `:bug:` - Bug fix
  - 📝 `:memo:` - Documentation
  - ♻️ `:recycle:` - Refactoring
  - ✅ `:white_check_mark:` - Tests
  - 🔧 `:wrench:` - Configuration
  - 🎨 `:art:` - Code style/formatting
- **Integration tests**: Can be separate commits if it makes sense

#### Commit Message Format
Follow these best practices for commit messages:
- **Limit subject line to 50 characters**
- **Capitalize only the first letter** in the subject line
- **No period** at the end of the subject line
- **Insert blank line** between subject line and body
- **Wrap body at 72 characters**
- **Use imperative mood** ("Add feature" not "Added feature")
- **Describe what and why**, not how

**Example:**
```
✨ Add memory store with cosine similarity

Implement associative memory storage using cosine similarity for
retrieval. This provides the foundation for the AMEM algorithm's
memory component.

- Support capacity-limited storage with FIFO eviction
- Include comprehensive error handling for dimension mismatches
- Add unit tests covering edge cases and error conditions
```

#### Git History Management
- **Clean commit history**: Use interactive rebase to create logical story
- **Squash related commits**: Combine WIP/fixup commits into meaningful units
- **Reorder commits**: Arrange commits in logical dependency order
- **Each commit must**:
  - Pass all pre-commit hooks (`pre-commit run --all-files`)
  - Pass all tests (`pytest`)
  - Be atomic and focused on single concern
  - Have proper commit message format

**Interactive rebase workflow:**
```bash
# Start interactive rebase from main branch
git rebase -i main

# Common rebase commands:
# pick = use commit as-is
# squash = combine with previous commit
# reword = change commit message
# edit = pause to modify commit
# drop = remove commit entirely

# After rebase, force push to feature branch
git push --force-with-lease origin feature-branch-name

# Verify each commit individually
git log --oneline main..HEAD
git show --name-only HEAD~2  # Check specific commit
```

#### Pull Request Guidelines
- **Small PRs**: Keep pull requests focused and small (ideally 2-5 commits)
- **Rare exceptions**: Only when there's strong logical sense for larger PRs
- **Atomic changes**: Each PR should implement one feature or fix
- **Complete documentation**: All code includes docstrings and tests
- **Clean history**: Rebase feature branch before creating PR
- **Linear history**: Avoid merge commits in feature branches

### Pre-commit Hooks
- Trailing whitespace and file fixes
- YAML validation
- Ruff linting and formatting
- MyPy type checking (excludes tests/)
- Unit test execution