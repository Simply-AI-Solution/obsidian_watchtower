# Contributing to Obsidian Watchtower

Thank you for your interest in contributing to Obsidian Watchtower! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- (Optional) PostgreSQL 12+ with pgvector extension

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Simply-AI-Solution/obsidian_watchtower.git
   cd obsidian_watchtower
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install dev dependencies
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## Code Standards

### Style Guide

- **Formatting**: Use Black with 100 character line length
  ```bash
  black watchtower tests
  ```

- **Linting**: Use Ruff for linting
  ```bash
  ruff watchtower tests
  ```

- **Type Checking**: Use mypy for type checking
  ```bash
  mypy watchtower
  ```

### Code Quality Checklist

Before submitting a PR, ensure:

- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black watchtower tests`
- [ ] No linting errors: `ruff watchtower tests`
- [ ] Type hints are present and valid: `mypy watchtower`
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_evidence.py

# Run with verbose output
pytest -v

# Run with coverage report
pip install pytest-cov
pytest --cov=watchtower --cov-report=html
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names: `test_<functionality>_<condition>_<expected_result>`
- Follow existing test patterns

Example:
```python
def test_evidence_creation() -> None:
    """Test basic evidence creation."""
    evidence = Evidence(
        content="Test content",
        source="manual"
    )
    assert evidence.content == "Test content"
    assert evidence.source == "manual"
```

## Pull Request Process

1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** with clear, focused commits
   ```bash
   git commit -m "Add feature X to improve Y"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

4. **Create a Pull Request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to any related issues
   - Screenshots for UI changes (if applicable)

5. **Address review feedback** if requested

### PR Review Criteria

PRs will be reviewed for:
- Code quality and style
- Test coverage
- Documentation updates
- Breaking changes (must be justified)
- Performance implications

## Feature Requests and Bug Reports

### Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version
- Operating system
- Relevant error messages or logs

### Feature Requests

For feature requests, please include:
- Problem you're trying to solve
- Proposed solution
- Alternative solutions considered
- Impact on existing functionality

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

## Development Workflow

### Branch Naming

- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring
- `test/*` - Test additions/improvements

### Commit Messages

Format: `<type>: <description>`

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation change
- `test:` - Test addition/modification
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

Example:
```
feat: Add support for PDF evidence extraction
fix: Correct SHA-256 computation for empty content
docs: Update README with installation instructions
```

## Areas for Contribution

### High Priority

- [ ] Neo4j/Apache AGE graph database integration
- [ ] Vector similarity search implementation
- [ ] Additional source plugins (web scraping, APIs)
- [ ] Enhanced visualization tools
- [ ] Performance optimizations

### Medium Priority

- [ ] Web UI for investigation management
- [ ] Real-time monitoring and alerting
- [ ] Export format improvements
- [ ] Advanced search capabilities
- [ ] Batch processing utilities

### Good First Issues

- [ ] Additional unit tests
- [ ] Documentation improvements
- [ ] Example scripts
- [ ] Bug fixes
- [ ] Code cleanup

## Documentation

### Types of Documentation

1. **API Documentation**: Docstrings in code
2. **User Documentation**: README.md
3. **Architecture Documentation**: ARCHITECTURE.md
4. **Contributing Guide**: This file

### Writing Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep examples up to date with API changes
- Use proper Markdown formatting

## Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers directly for sensitive issues

## License

By contributing to Obsidian Watchtower, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in release notes
- Mentioned in the README (for significant contributions)
- Given credit in commit history

Thank you for contributing to Obsidian Watchtower! 🎉
