# Summarizer Agent - Contributing Guide

Thank you for your interest in contributing to the Summarizer Agent project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python and project styleguides
* Include appropriate test cases
* Document new code based on the documentation styleguide
* End all files with a newline

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/parasgor/SummarizerProject.git
   cd SummarizerProject
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov pytest-mock black flake8 mypy isort
   ```

5. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style Guide

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:

* Maximum line length: 120 characters
* Use 4 spaces for indentation
* Use type hints for function parameters and return types
* Use docstrings for all public modules, functions, classes, and methods

### Code Formatting

We use `black` for code formatting:

```bash
black src/ tests/
```

### Import Sorting

We use `isort` to sort imports:

```bash
isort src/ tests/
```

### Type Checking

We use `mypy` for static type checking:

```bash
mypy src/
```

### Linting

We use `flake8` for linting:

```bash
flake8 src/ tests/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agent.py

# Run with verbose output
pytest -v
```

### Writing Tests

* Write tests for all new features
* Aim for at least 80% code coverage
* Use descriptive test names
* Use fixtures for common setup
* Mock external API calls

Example test:

```python
def test_summarize_valid_text(self, mock_openai):
    """Test summarizing valid text."""
    # Arrange
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = Mock()
    mock_response.choices[0].message.content = "This is a summary."
    mock_client.chat.completions.create.return_value = mock_response
    
    # Act
    agent = SummarizerAgent()
    result = agent.summarize("This is a long text that needs to be summarized.")
    
    # Assert
    assert result == "This is a summary."
```

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
  - 🎨 when improving the format/structure of the code
  - ⚡ when improving performance
  - 📝 when writing docs
  - 🐛 when fixing a bug
  - ✨ when introducing a new feature
  - 🔒 when dealing with security
  - ⬆️ when upgrading dependencies
  - ⬇️ when downgrading dependencies
  - 🔧 when updating configuration files

## Documentation

* Update README.md if you add/change functionality
* Include docstrings for new functions and classes
* Use type hints
* Add examples for complex functionality

### Docstring Format

```python
def summarize(self, text: str, prompt: Optional[str] = None) -> str:
    """
    Summarize a single text.
    
    Args:
        text: Text to summarize
        prompt: Custom summarization prompt (optional)
    
    Returns:
        Generated summary
    
    Raises:
        ValueError: If text is invalid
        Exception: If API call fails
    """
```

## Release Process

1. Update version number in `setup.py` and `src/__init__.py`
2. Update CHANGELOG.md
3. Create a git tag: `git tag v1.0.0`
4. Push to repository: `git push origin main --tags`
5. Create release on GitHub with release notes

## Additional Notes

* Check the existing issues before working on something
* Discuss major changes in an issue first
* Be respectful and constructive in all interactions
* Follow the existing code patterns and conventions

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

---

Thank you for contributing! 🎉
