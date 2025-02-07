# Development Guidelines

## Introduction
This document serves as a comprehensive guide for development practices and standards. It is a living document that will evolve throughout the development process.

## Table of Contents
- [Introduction](#introduction)
- [Code Quality Standards](#code-quality-standards)
  - [Naming Conventions](#naming-conventions)
  - [Documentation](#documentation)
  - [Testing](#testing)
- [Version Control](#version-control)
  - [Branching Strategy](#branching-strategy)
  - [Pull Request Guidelines](#pull-request-guidelines)
  - [Code Review Process](#code-review-process)

## Code Quality Standards

### Naming Conventions
> Note: To be completed with team consensus

Key principles to consider:
- Use meaningful and descriptive names
- Follow language-specific conventions
- Maintain consistency across the codebase

### Documentation

#### Method and Class Documentation
All public-facing methods and classes must include:
- Description of functionality
- Input parameters and their types
- Return values and types
- Any exceptions that may be thrown
- Usage examples where appropriate

Documentation should use standard markup for automatic documentation generation:
- Python: Pydoc
- JavaScript: JSDoc
- C#: XML Documentation Comments

Example:

```python
class Calculator:
    """
    Provides basic mathematical operations with input validation.
    """

    def multiply(self, x: float, y: float) -> float:
        """
        Multiplies two numbers and returns their product.

        Args:
            x (float): First number
            y (float): Second number

        Returns:
            float: Product of x and y

        Raises:
            TypeError: If inputs are not numbers
        """
        if not all(isinstance(i, (int, float)) for i in [x, y]):
            raise TypeError("Inputs must be numbers")
        return x * y
```

### Testing

#### Test Organization
Tests should be organized in a separate directory mirroring the main project structure:

```
project_root/
├── src/
│   ├── calculator.py
│   └── validator.py
└── tests/
    ├── test_calculator.py
    └── test_validator.py
```

#### Writing Tests
Follow the Arrange-Act-Assert pattern:

```python
import pytest
from src.calculator import Calculator

def test_multiply_positive_numbers():
    # Arrange
    calc = Calculator()
    x, y = 2.0, 3.0
    expected = 6.0

    # Act
    result = calc.multiply(x, y)

    # Assert
    assert result == expected
```

## Version Control

### Branching Strategy

#### A Real-World Example
Mr Mundray is allocated `Issue #189`: to build a new API endpoint on the toaster service. As the toaster service already exists, it is in the branch `project/toaster`.

Therefore, he follows these steps:
1. Creates the branch `feature/toaster_189` from `project/toaster`
2. Completes the work, including unit tests
3. Creates a Pull Request to merge his work into `project/toaster`
4. Gets two developers to review his work
5. After approval, completes the merge and deletes `feature/toaster_189`

#### Branch Types
- Main branches: `main`, `development`
- Feature branches: `feature/<component>_<issue-number>`
- Bug fix branches: `bugfix/<component>_<issue-number>`
- Project branches: `project/<component-name>`

### Pull Request Guidelines

#### Required Components
- Descriptive title (can reference ticket number)
- Summary of changes
- Links to related issues
- Test coverage information
- Any deployment considerations

#### Example Pull Request Template
```markdown
## Description
[Brief description of changes]

## Related Issues
- #189: Add new toaster API endpoint

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tested in development environment

## Additional Notes
[Any deployment steps or considerations]
```

### Code Review Process

#### Requirements
- Minimum two approvals from other developers
- All automated tests must pass
- Code coverage requirements met
- No unresolved comments

#### Review Guidelines
1. Review code thoroughly
2. Check for:
   - Proper test coverage
   - Documentation completeness
   - Code style consistency
   - Potential security issues
   - Performance implications
3. Provide constructive feedback
4. Verify all acceptance criteria are met

## Appendix

OpenAI's ChatGPT GPT-4-turbo model was used to assist in generating examples for this wiki. [The full chat can be found here.](https://chatgpt.com/share/679fb52b-e050-8007-b826-53a3871afa0e)