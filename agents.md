## Python 3.10+ Code Style Guide (Standalone & LLM Optimized)

**Core Objective:** Maximize code readability and maintainability for long-term project health, leveraging Python 3.10+ features and best practices.

---
## Clarity and Simplicity

* **Fundamental Rule: Maximize Understandability.** All code MUST be written to minimize the cognitive effort required for another developer (or an AI agent) to understand it. This is the paramount principle.
* **Keep it Simple (KISS Principle).** Code MUST be the simplest possible Pythonic solution that correctly and completely solves the problem. AVOID overly simplistic code that ignores necessary complexities or error conditions. Simplicity is not an excuse for incorrectness.
* **Single Responsibility.** Each function, method, class, and logical code paragraph SHOULD perform only one distinct task. (This is the Single Responsibility Principle (SRP) detailed in "Design Principles (SOLID)").
* **Prefer Immutability.** Where practical and idiomatic for Python, PREFER immutable data structures (e.g., tuples, frozensets) and design objects to be immutable if their state is not meant to change post-creation. This simplifies state management, reduces side effects, and aids reasoning. Consider libraries like `attrs` with `frozen=True` or dataclasses with `frozen=True`.
* **Avoid "Clever" Code.** AVOID overly concise or obscure code that is difficult to read, understand, or debug. Prioritize clarity over esoteric language features.
* **Minimize Nesting Depth.** Deeply nested control structures hinder understanding. REFACTOR to reduce nesting using techniques such as early returns, guard clauses, or `continue` statements.
* **Pythonic Idioms and Comprehensions:**
    * Write idiomatic Python.
    * **PREFER comprehensions (list, set, dict) and generator expressions** over `map()` and `filter()` for creating collections or iterating.
    * For complex loop logic building a new collection, a helper function within a comprehension is PREFERRED over a multi-line loop if it enhances clarity.
    * **Leverage Standard Library and Trusted Packages:**
        * Utilize the Python Standard Library effectively.
        * Use `numpy` for numerical operations and `more_itertools` for advanced iteration patterns where appropriate and they simplify code or improve performance.

---
## Design Principles (SOLID)

The SOLID principles provide a framework for designing robust, maintainable, and flexible Python software. Their core concepts are valuable across programming paradigms.

* **S - Single Responsibility Principle (SRP):**
    * A class, module, function, or method SHOULD have only one reason to change, meaning it should have only one primary responsibility.
* **O - Open/Closed Principle (OCP):**
    * Software entities SHOULD be open for extension but closed for modification.
    * In Python, achieve this via inheritance, composition, dependency injection, or functions accepting plugins/strategies (e.g., first-class functions).
* **L - Liskov Substitution Principle (LSP):**
    * Subtypes MUST be substitutable for their base types without altering program correctness. If code works with a base class/interface (Protocol/ABC), it MUST also work with its derivatives.
* **I - Interface Segregation Principle (ISP):**
    * Clients SHOULD NOT be forced to depend on interfaces (Protocols/ABCs in Python) they do not use. PREFER many small, cohesive interfaces/Protocols over large ones.
    * **`typing.Protocol` vs. `abc.ABC` Choice in Python:**
        * `typing.Protocol`: For structural subtyping (implicit interface implementation by matching structure). Use when explicit inheritance is not desired/possible, or for adapting existing classes.
        * `abc.ABC`: For nominal subtyping (explicit inheritance via `class MyClass(MyABC):`). Use to provide common concrete implementations, enforce a stronger contractual relationship, or when `isinstance()` checks are crucial for the abstraction.
* **D - Dependency Inversion Principle (DIP):**
    * High-level modules SHOULD NOT depend on low-level modules. Both SHOULD depend on abstractions (e.g., interfaces, Protocols, ABCs in Python).
    * Abstractions SHOULD NOT depend on details. Details (concrete implementations) SHOULD depend on abstractions.
    * **Dependency Injection (DI) in Python:** Implement by supplying dependencies to objects via constructors (preferred) or methods, not by internal instantiation of complex dependencies. This promotes loose coupling, enhances testability, and allows for flexibility.
        * For small projects, manual DI (passing objects directly) is standard and often sufficient.
        * For larger projects or complex DI scenarios, consider using a DI framework like `dependency-injector`.
* **Balancing Paradigms:** Python is multi-paradigm. The choice between functional (e.g., first-class functions, immutability, comprehensions), OOP, or a hybrid approach MUST be driven by:
    1.  Idiomatic Python practices for the specific problem.
    2.  The nature and complexity of the problem.
    3.  The paramount goal of maximizing understandability and maintainability.
    Generate the simplest, clearest, and most robust Pythonic solution.

---
## Type Hinting (PEP 484 and newer)

Static type hinting improves code clarity, enables static analysis, and reduces bugs.

* **Mandatory Type Hints:** All new Python 3.10+ code MUST include type hints for function arguments, return types, and variable assignments where appropriate.
* **Tooling:** `Mypy` (integrated with `ruff`) MUST be used in pre-commit hooks for static type analysis and correctness enforcement.
* **Built-in Generic Types:** For Python 3.9+, use built-in collection types as generics directly (e.g., `list[int]`, `dict[str, float]`, `set[MyClass]`).
* **Clarity and Precision:** Type hints MUST be as precise as possible. Use `typing.Optional[X]` or the `X | None` union syntax (Python 3.10+) for values that can be `X` or `None`.
* **Protocols vs. ABCs:** Choose `typing.Protocol` for structural subtyping and `abc.ABC` for nominal subtyping as per ISP/DIP guidelines.
* **`typing.Any`:** Use `Any` sparingly, only when no other more specific type is appropriate. Its use disables type checking for that part.
* **Forward References:** Use string literals for forward references if a type is not yet defined (e.g., `attribute: 'MyDefiningClass'`). `from __future__ import annotations` (standard in Python 3.11+) can simplify this.

---
## Naming Conventions (PEP 8)

Adhere to PEP 8 naming conventions for consistency and readability.

* **Descriptive Names.** Names MUST be specific and clearly describe the entity's purpose or the value it holds.
* **Avoid Generic Names.** AVOID names like `tmp`, `retval`, `data`, `info`, `foo`, except for very short-lived variables with unequivocally clear context.
* **Prefer Concrete and Specific Names.** Names SHOULD describe things concretely rather than abstractly (e.g., `CanListenOnPort()` is preferred over `ServerCanStart()` if the specific check is about port listening).
* **Boolean Variable and Function Naming.**
    * Names for boolean entities MUST clearly indicate what `true` and `false` represent.
    * PREFER prefixes like `is_`, `has_`, `can_`, or `should_` (e.g., `is_active`, `has_permission`).
    * AVOID negated terms in names (e.g., use `is_user_active` instead of `is_user_inactive`; use `enable_feature` instead of `disable_feature_is_false`).
* **Function/Method Naming.**
    * Name functions and methods based on their logical operation or effect, from an external viewpoint, not their internal implementation. Names SHOULD typically include a verb.
    * Follow `snake_case` (e.g., `calculate_total`, `get_user_data`).
* **Name Length and Scope.**
    * Shorter names are acceptable for variables with very small scopes where context is immediately obvious.
    * Longer, more descriptive names ARE REQUIRED for entities with larger scopes or when clarity demands it.
* **Consistent Formatting for Meaning (PEP 8):**
    * `snake_case`: For functions, methods, variables, and module names.
    * `PascalCase` (CapWords): For class names.
    * `CONSTANT_CASE` (all uppercase with underscores): For constants.
    * `_internal_use`: Single leading underscore as a weak "internal use" indicator for variables/methods.
    * `__name_mangling`: Double leading underscore for mangling class attributes (use with care, primarily for avoiding name clashes in inheritance).

---
## Comments and Docstrings (PEP 257)

Comments explain the "why" and context; code explains the "how". Docstrings are mandatory for public APIs.

* **Primary Purpose of Comments.** Comments MUST provide understanding of design choices, trade-offs, and context not immediately obvious from the code.
* **Comment When Code Clarity Is Insufficient.** Prefer improving code clarity (e.g., better naming, refactoring) over adding comments.
* **Docstrings (PEP 257):**
    * **Every public module, function, class, and method MUST have a docstring.**
    * Docstrings are string literals as the first statement in the definition.
    * **Module Docstrings:** Explain the module's purpose and any important classes or functions it exports.
    * **Class Docstrings:** Summarize its behavior and list public methods and instance variables.
    * **Function/Method Docstrings:**
        * Start with a concise summary line (imperative mood, e.g., "Return the frobnicator.").
        * Follow with a more detailed explanation if necessary, describing arguments (and their types if not obvious from hints), return values (and type), side effects, exceptions raised (e.g., using `Raises:` section), and restrictions.
        * Use a standard format (e.g., Google Python Style, reStructuredText, NumPy/SciPy) for consistency and to support automated documentation generation (e.g., with Sphinx).
* **Guidance on What to Comment (Inline Comments):**
    * Decisions: Record insights into design choices or alternative approaches considered and why the current one was chosen.
    * Flaws/TODOs: Document known issues or future work using `TODO:`, `FIXME:`, `XXX:`, with explanations.
    * Constants: Explain the meaning of constants, their intended use, and limitations if not obvious (often better in docstrings if module/class constants).
    * Anticipated Confusion & Pitfalls: Proactively comment on potentially confusing code sections or warn about non-obvious side effects.
    * High-Level Structure & Summaries: Use comments for overall architecture summaries if not covered by module/class docstrings, or to summarize complex code blocks.
* **Guidance on What NOT to Comment:**
    * Obvious Facts: AVOID comments that restate what the code clearly does.
    * Bad Names: Do NOT use comments to explain a poorly chosen name; FIX the name.
* **Precision, Conciseness, and Synchronization.**
    * Comments/docstrings MUST be precise, concise, grammatically correct, and clearly phrased. AVOID ambiguous pronouns.
    * Focus on Intent ("Why"): Comments SHOULD explain high-level intent, not just low-level mechanics, unless the "how" is particularly complex.
    * **Keep Comments/Docstrings Synchronized:** Comments and docstrings MUST be kept up-to-date with corresponding code changes.

---
## Formatting and Aesthetics (PEP 8 & Ruff)

Adherence to PEP 8, enforced by Ruff, is standard.

* **Adhere to PEP 8.** PEP 8 is the primary style guide for Python code.
* **Tooling: Ruff and Pre-commit Hooks:**
    * **Ruff MUST be used as the primary tool for linting and formatting Python code.** (Covers Flake8, isort, pydocstyle, Black functionalities).
    * Configure Ruff according to project standards via `pyproject.toml` or `ruff.toml`.
    * **Ruff (and Mypy) MUST be integrated into pre-commit hooks** to ensure code is checked and formatted before being committed.
* **Consistency is Key.** A consistent coding style (as defined by PEP 8 and Ruff auto-formatting) MUST be maintained throughout the project.
* **Visually Similar Structures for Similar Logic.** Format similar logical blocks of code identically or very similarly.
* **Meaningful Order and Logical Grouping.** Organize declarations and code into logical blocks, separated by empty lines. Ruff handles import sorting per PEP 8 guidelines (stdlib, then third-party, then local, each group alphabetized). Within functions/methods, group related operations.
* **Column Alignment:** AVOID excessive column alignment that makes code modification difficult. Ruff's formatter generally discourages this.

---
## Error Handling and Robustness Rules

Prioritize the **fail-fast principle**.

* **Prioritize Fail-Fast.** Operations MUST terminate immediately and report an error upon encountering an unrecoverable situation or one that would leave the system in an inconsistent or unstable state. This prevents further incorrect computations and aids quicker diagnostics.
* **Validate Inputs Rigorously and Early.** All external inputs, arguments to public functions/methods, and configuration values MUST be validated at the earliest possible point. Assume no input is safe until validated.
* **Handle or Propagate Errors—Never Ignore.** Errors or exceptions MUST NOT be silently ignored (e.g., `except: pass` or empty `except Exception:`). If a component cannot handle an error, it MUST propagate it.
* **Catch Specific Exceptions.** Always catch the most specific exception type(s) relevant (e.g., `except ValueError:`, `except (KeyError, IndexError):`). AVOID catching generic `Exception` or using a bare `except:` unless re-throwing or for top-level error handling/logging.
* **Ensure Resource Cleanup.** Acquired resources (files, connections, locks) MUST be reliably released. Use `try...finally` blocks or, PREFERABLY, context managers (`with` statement).
* **Provide Clear and Contextual Error Information.** Error messages (logs or exceptions) MUST be clear, informative, and provide context (what, where, why).
* **Use Custom Exceptions for Application-Specific Errors.** Define and use specific custom exception classes (inheriting from `Exception` or more specific built-ins) for distinct application-level error conditions.
* **Do Not Use Exceptions for Normal Control Flow.** Exceptions MUST only be used for genuinely exceptional, unexpected error conditions.
* **Log Errors Effectively.** When an error is handled or propagated, log sufficient details for post-mortem analysis using the standard Python `logging` module. Logging is a diagnostic aid, not error handling itself.
* **Maintain Exception Abstraction Levels.** Exceptions caught and re-thrown SHOULD be appropriate to the current abstraction level. Consider wrapping lower-level exceptions in a type meaningful to the current layer if necessary.
* **Handle Asynchronous Operations Carefully (asyncio).** Ensure all outcomes (success, error) of `async` operations are explicitly handled. Propagate errors correctly through asynchronous call chains (e.g., by `await`ing tasks). Manage resources and AVOID race conditions/deadlocks.

---
## Secure Coding Practices

Protect data and system integrity.

* **Validate Inputs for Security:** All external inputs (APIs, user inputs, config files) MUST be validated against common security vulnerabilities (e.g., SQL injection, XSS, command injection, path traversal, insecure deserialization). Assume all input is malicious until validated. Use libraries or established patterns.
* **Principle of Least Privilege:** Code and processes SHOULD operate with the minimum permissions necessary.
* **Avoid Hardcoded Secrets:** API keys, passwords, etc., MUST NOT be in source code. Use environment variables (e.g., via Dynaconf from secure sources) or dedicated secret management tools.
* **Keep Dependencies Updated and Scanned:** Regularly update dependencies and scan them for vulnerabilities (e.g., using `pip-tools` or Poetry/PDM update mechanisms, and `pip-audit` or GitHub Dependabot).
* **Sanitize Outputs:** Ensure user-supplied data is properly sanitized/escaped before display or use in other systems to prevent XSS. Use libraries like `bleach` for HTML.
* **Secure by Default:** Design APIs and systems with secure default configurations.
* **Deserialization Security:** AVOID `pickle` for untrusted data. Use safer formats like JSON. If `pickle` is unavoidable, ensure data source is trusted.
* **YAML Loading Security:** ALWAYS use `yaml.safe_load()` instead of `yaml.load()` to prevent arbitrary code execution.

---
## Testing Rules (Pytest)

**Pytest is the standard testing framework.** Adherence is mandatory for software quality.

* **Design for Testability.** Code MUST be written with testability as a core consideration. PREFER modular, decoupled designs with clear interfaces. Adhering to SOLID principles (especially DIP for mocking) is crucial for testability.

* **Test File and Directory Structure:**
    * Tests reside in a `tests/` directory at the project root.
    * **Separate tests by type:** `tests/unit/`, `tests/integration/`, `tests/e2e/`.
    * Test filenames MUST ends with `test_` (e.g., `user_model_test.py`).
    * Test function names MUST start with `test_` (e.g., `def test_user_creation_success():`).
    * Test class names (if grouping tests, though often not necessary with pytest) SHOULD start with `Test`.

### Unit Testing (UT)

Fundamental for all new or modified code.

* **Co-Development and Commit of Tests:** UTs MUST be written with features/fixes and committed atomically with the functional code.
* **Scope and Isolation:** Each test MUST focus on a single logical behavior of the unit. Isolate the unit from external dependencies using test doubles (mocks, stubs, fakes).
    * **Use `pytest-mock` (via the `mocker` fixture)** for creating mocks, stubs, and fakes.
* **Readability and Maintainability of Tests:** Test code MUST be as readable and maintainable as production code. Use clear, descriptive names.
* **AAA Pattern (Arrange, Act, Assert):** All UTs MUST be structured using this pattern:
    * **Arrange:** Set up preconditions, inputs, mock expectations.
    * **Act:** Execute the unit of code.
    * **Assert:** Verify outcomes match expectations. Use specific assertion methods.
* **Comprehensive Coverage:** Tests MUST cover "happy path" scenarios, edge cases, boundary conditions, invalid inputs, and error handling paths.
* **Execution Requirements:** UTs MUST be fast, fully automated, and pass before code is committed or merged.
* **Focus of Tests:**
    * Do NOT test trivial code (e.g., simple getters/setters without logic).
    * Do NOT test functionality of external libraries unless testing your specific integration contract or wrapper.
    * Aim for one logical assertion per test case where feasible. Multiple physical assertions are acceptable if cohesively testing a single logical outcome.
* **Test Data Minimization:** Use the simplest, minimal data required for the specific scenario. Helper fixtures MAY reduce boilerplate but ensure test intent remains clear.
* **Pytest Features:**
    * Use plain `assert` statements for Python's rich introspection.
    * Use fixtures extensively for managing test dependencies and setup/teardown logic.
    * Use parametrization (`@pytest.mark.parametrize`) to test multiple input/output scenarios efficiently.
    * Use markers (`@pytest.mark`) for organizing, categorizing (e.g., `@pytest.mark.slow`), and selectively running tests.

### Integration Testing (IT)

Ensures different components/modules/services interact correctly.

* **Purpose:** Verify interactions and data flow between distinct internal modules/services (e.g., API calls between internal services, database interactions via data access layer, message queue communication).
* **Scope:** Focus on the interface points, contracts, and data exchange between integrated components.
* **Management of External Dependencies:**
    * When testing interactions between *your own* application components, you MAY use test doubles (e.g., `pytest-mock`) for *true third-party* external services (e.g., external payment gateways) for stability and control.
    * For databases, tests SHOULD run against a dedicated test database instance, not production. Consider libraries like `pytest-postgresql` or `pytest-docker` for managing test databases.
* **Data Management:** Implement reliable mechanisms for test data setup and teardown.
* **Automation & CI:** ITs MUST be automated and included in CI/CD pipeline. They may run less frequently than UTs if significantly slower.
* **Commitment with Features:** ITs for a feature SHOULD ideally be in the same commit or a closely following commit.

### End-to-End (E2E) Testing 🌐

Validates complete application flows from a user's perspective.

* **Focus on User Journeys:** Define E2E tests based on critical user scenarios or workflows.
* **Verification of Real Third-Party Service Communication:** E2E tests MUST verify actual communication, contracts, and interactions with essential live or production-like third-party services where practical and typically mocked elsewhere. This ensures real-world interoperability.
* **Test Environment:** E2E tests MUST execute in an environment mirroring production closely.
* **Selectivity and Prioritization:** Due to potential slowness, cost, and brittleness, E2E tests MUST be reserved for the most critical end-to-end functionalities.
* **Data Integrity for E2E Tests:** Establish robust strategies for managing test data across the entire application stack for E2E tests to ensure consistency, reliability, and repeatability.
* **Useful Pytest Extensions:** Explore and use other pytest extensions as needed (e.g., for time mocking like `freezegun` via `pytest-freezegun`, API testing, database interaction).

---
## Code Management and Evolution

* **Project Structure and Packaging:**
    * **All projects MUST be organized as installable Python packages.** This means including a `pyproject.toml` file and a proper package layout (e.g., `src/your_package_name` or `your_package_name/` at the root).
    * **Use `pyproject.toml` (PEP 518, PEP 621) for defining project metadata, dependencies, and build system configuration.**
    * PREFER modern build backends like `hatchling`, `setuptools` (with configuration in `pyproject.toml`), or `poetry-core`.
    * Manage development environments and dependencies using tools like `pip` with `venv`, `Poetry`, or `PDM`. Ensure consistency within a project.
* **Versioning:**
    * Package versions SHOULD be managed using a tool that derives the version from SCM (Source Code Management, i.e., Git) tags, such as `setuptools_scm` or `hatch-vcs`. This ensures versions are tied to Git history and facilitates automated versioning.
* **Write Less Code (YAGNI - You Ain't Gonna Need It).** Do NOT implement features or abstractions not currently needed.
* **Continuous Refactoring.** Continuously improve internal code structure and clarity without changing external behavior to make code easier to understand, modify, and test.
* **Remove Dead Code.** Actively delete unused code. Rely on version control for history.
* **API Design and Documentation:**
    * **Apply SOLID Principles:** The SOLID design principles (see "Design Principles (SOLID)") SHOULD be applied when designing APIs.
    * **Design for Usability:** APIs (libraries, services) MUST be designed to be intuitive, consistent, discoverable, and predictable.
    * **Follow Conventions:** Adhere to established Pythonic API design conventions and RESTful principles for HTTP APIs.
    * **Clear Contracts:** Define clear contracts for API requests and responses, including data formats (enforced/documented via type hints and docstrings), status codes (for services), and error structures.
    * **Versioning:** Implement an API versioning strategy early in the design process for services expected to evolve.
    * **Documentation Generation:** For public APIs, use Sphinx with appropriate extensions (e.g., `sphinx.ext.autodoc`, `sphinx.ext.napoleon`, `sphinx-autoapi`) to generate API documentation from Python docstrings. Documentation should cover endpoints, parameters, return values, error conditions, and usage examples.
* **Consider Performance Mindfully.** Write correct, clear Python code first. Profile (e.g., using `cProfile`, `line_profiler`, `scalene`) to identify actual bottlenecks before optimizing. Optimize critical sections only when necessary and backed by data. AVOID premature optimization.
* **Externalize Configuration:**
    * Configuration (DB connection strings, API endpoints, feature flags, tunable parameters) MUST be externalized from code.
    * **Utilize Dynaconf for managing configuration.** Store primary configuration in `config.yaml` (and potentially `.secrets.yaml` for development secrets, which MUST be gitignored).
    * Dynaconf settings SHOULD be overridable by environment variables for deployment flexibility (dev, staging, prod).
    * For larger projects, **implement configuration migrations** or a clear strategy for managing changes in configuration structure/defaults over time.
* **Data Access (SQLAlchemy):**
    * **Use SQLAlchemy for abstracting database access.**
    * **SQLAlchemy Core vs. ORM Choice:**
        * **Core:** For direct SQL control, highly optimized/complex queries, or a lighter abstraction. Use when SQL fluency is high and fine-grained control is needed.
        * **ORM:** For higher-level object mapping, potentially faster development for CRUD operations and managing object relationships. Use when object-centric interaction is preferred.
        * Base choice on project complexity, performance needs, data model complexity, and team familiarity/preference. It's also possible to use both within the same project.
    * **For projects with evolving database schemas, Alembic MUST be used for database migrations.** Alembic integrates with SQLAlchemy to manage schema changes systematically.

---
## Version Control Rules (Git)

Maintain a clear, understandable, navigable project history using Git.

* **Atomic Commits.**
    * Each commit MUST represent a single, complete logical change (e.g., a feature, a bug fix, a refactor). This makes changes easier to understand, review, and revert if necessary.
    * AVOID lumping unrelated changes. Implementation and its corresponding tests MUST be in the same commit.
* **Ensure Tests Pass Before Commit.** All automated tests (unit, relevant integration) MUST pass before code is committed to a shared branch (enforced by pre-commit hooks). Do NOT commit broken code.
* **Clear and Concise Commit Messages.** Messages MUST explain *what* change was made and *why*. Adhere to Conventional Commits format if adopted by the project.
    * **Subject Line Rules:**
        * Limit to ~50 chars.
        * Capitalize like a sentence.
        * No period at the end.
        * Imperative mood (e.g., "Add user login endpoint").
    * **Body Rules (Recommended for non-trivial changes):**
        * Separate from subject with a blank line.
        * Wrap at ~72 chars.
        * Explain "what" and "why". AVOID detailing "how" if evident from code.
        * MAY include issue references.
* **Example of a Good Commit Message:**
    ```
    feat: Add user authentication endpoint

    Implement the /login endpoint allowing users to authenticate
    using their username and password via JWT.

    This addresses issue #123 and is the foundational step
    towards securing user-specific data access. It uses the
    existing AuthService for credential validation.
    ```
* **Use `gitmoji` (Optional but Encouraged for Consistency if Adopted).** If the project uses `gitmoji`, prefix commit messages with the appropriate emoji to provide a quick visual cue of the commit's purpose. Examples:
    * 🎉 `:tada:` - Initial commit
    * ✨ `:sparkles:` - New feature
    * 🐛 `:bug:` - Bug fix
    * 📝 `:memo:` - Documentation
    * ♻️ `:recycle:` - Refactoring
    * ✅ `:white_check_mark:` - Adding or updating tests
    * 🔧 `:wrench:` - Configuration changes
    * 🎨 `:art:` - Code style/formatting improvements
* **Branching Strategy.**
    * Use a consistent strategy (e.g., feature branches, Gitflow).
    * Feature branches SHOULD be short-lived and focused on a single piece of functionality.
    * The main branch (`main` or `master`) MUST always be stable and releasable.
* **Define Merge/Integration Strategy.** Establish a clear and consistent strategy for integrating feature branches (e.g., rebase then merge, squash merges). The chosen strategy should be documented and followed.
* **Pull Requests (PRs) / Merge Requests (MRs).**
    * PR/MR descriptions MUST be clear, provide context ("what" and "why"), and reference relevant issues.
    * PRs/MRs SHOULD be reviewed before merging.
    * **Scope of Review:** Reviewers (human or AI) SHOULD verify adherence to coding style (Ruff, Mypy), correctness, test coverage, security implications, performance, and overall design. Confirm alignment with stated purpose.

