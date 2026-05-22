# Contributing Guide

Guidelines for contributing to the B-Bot project.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Supabase account (for local development)
- Familiarity with Flask, Python, and web development

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/your-username/B-Bot.git
cd B-Bot
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

6. Run tests to verify setup:
```bash
pytest tests/ -v
```

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Urgent production fixes

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in the feature branch
2. Write tests for new functionality
3. Ensure all tests pass:
```bash
pytest tests/ -v
```
4. Commit your changes with descriptive messages:
```bash
git add .
git commit -m "Add feature: description of what you did"
```

### Commit Message Format

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting)
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

Examples:
```
feat(interpreter): add support for while loops
fix(auth): resolve token refresh issue
docs(api): update endpoint documentation
```

### Pull Request Process

1. Push your branch:
```bash
git push origin feature/your-feature-name
```

2. Create a pull request on GitHub
3. Fill out the PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if applicable)

4. Request review from maintainers

5. Address review feedback

6. Once approved, merge into `develop`

## Code Style Guidelines

### Python Code Style

Follow PEP 8 guidelines:

- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use snake_case for variables and functions
- Use PascalCase for classes
- Use UPPER_CASE for constants

### Example

```python
# Good
def calculate_distance(x1, y1, x2, y2):
    """Calculate the distance between two points."""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Bad
def CalculateDistance(x,y,X,Y):
    return ((X-x)**2+(Y-y)**2)**0.5
```

### Documentation

Add docstrings to all functions and classes:

```python
def execute_script(script: str, timeout: int = 5) -> List[Dict]:
    """
    Execute a user script with timeout protection.
    
    Args:
        script: The Python script to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        List of command dictionaries
        
    Raises:
        ScriptValidationError: If script execution fails
    """
    pass
```

### Type Hints

Use type hints for function signatures:

```python
from typing import List, Dict, Optional

def process_commands(commands: List[Dict[str, Any]]) -> Optional[str]:
    pass
```

### Imports

Order imports:

1. Standard library imports
2. Third-party imports
3. Local imports

```python
import os
import sys

from flask import Flask, request
from RestrictedPython import compile_restricted

from core.interpreter import ScriptInterpreter
from core.security import decode_token
```

## Testing Guidelines

### Write Tests for New Features

Every new feature should include tests:

- Unit tests for individual functions
- Integration tests for component interactions
- Security tests for interpreter changes

### Test Coverage

Aim for:
- Core interpreter: 90%+ coverage
- Routes: 80%+ coverage
- Overall: 85%+ coverage

### Running Tests

Before submitting a PR, run:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov=routes

# Run specific test file
pytest tests/test_interpreter_functionality.py -v
```

## Security Guidelines

### Security Reviews

Any changes to the interpreter or security model require:
- Security review by maintainers
- Additional security tests
- Documentation updates

### Blocked Operations

Never remove security restrictions:
- Keep import blocking
- Maintain file operation blocking
- Preserve eval/exec blocking
- Keep timeout protection

### Reporting Security Issues

For security vulnerabilities:
- Do not open a public issue
- Contact maintainers privately
- Provide detailed information
- Allow time for fix before disclosure

## Documentation Guidelines

### Update Documentation

When adding features:
- Update the [Scripting Guide](scripting-guide.md)
- Update the [API Reference](api.md) if adding endpoints
- Update the [Architecture](architecture.md) if changing structure
- Update the [Security](security.md) if changing security model

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams for complex concepts (ASCII art)
- Keep user-facing docs simple
- Keep technical docs detailed

## Project Structure

```
B-Bot/
├── core/                     # Core application logic
│   ├── interpreter/          # Script interpreter
│   ├── config.py             # Configuration
│   ├── database.py           # Database client
│   └── security.py           # Authentication
├── routes/                   # Flask routes
│   ├── auth.py               # Authentication endpoints
│   └── simulation.py        # Game simulation endpoints
├── templates/                # Jinja2 templates
├── static/                   # Static assets
├── tests/                    # Test suite
├── docs/                     # Documentation
└── requirements.txt          # Dependencies
```

## Issue Reporting

### Before Creating an Issue

1. Search existing issues
2. Check if the issue is already reported
3. Gather relevant information

### Issue Template

```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- OS:
- Browser (if applicable):

## Additional Context
Logs, screenshots, or other relevant information
```

## Feature Requests

### Before Requesting a Feature

1. Check if the feature already exists
2. Search for similar requests
3. Consider if it fits the project scope

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Solution
How you envision the feature working

## Alternatives
Alternative approaches considered

## Additional Context
Examples, mockups, or references
```

## Code Review Guidelines

### Reviewing PRs

When reviewing pull requests:
- Check code follows style guidelines
- Verify tests are included and passing
- Ensure documentation is updated
- Check for security implications
- Test the changes locally if possible

### Receiving Reviews

When your PR is reviewed:
- Address feedback promptly
- Ask for clarification if needed
- Be open to suggestions
- Update tests and documentation as needed

## Release Process

### Versioning

Follow semantic versioning:
- MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number updated
- [ ] Tagged in Git
- [ ] Deployed to production

## Getting Help

### Channels

- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - Questions and ideas
- Documentation - Reference guides

### Asking Questions

When asking for help:
- Provide context about what you're trying to do
- Share relevant code snippets
- Include error messages
- Mention what you've already tried

## License

By contributing to B-Bot, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to B-Bot!
