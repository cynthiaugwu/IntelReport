# Contributing to IntelliReport

🎉 Thank you for considering contributing to IntelliReport! We welcome contributions from the community and are excited to work with you to improve intelligence report processing capabilities.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Contributing Guidelines](#contributing-guidelines)
- [Types of Contributions](#types-of-contributions)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project follows the IJEOMA Safety Platform Code of Conduct. By participating, you agree to uphold this code. Please report unacceptable behavior to [conduct@ijeoma.safety](mailto:conduct@ijeoma.safety).

### Our Standards

- **Respectful Communication**: Use welcoming and inclusive language
- **Constructive Feedback**: Focus on the code/ideas, not the person
- **Collaborative Spirit**: Work together toward common goals
- **Professional Conduct**: Maintain professionalism in all interactions

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Anthropic API key (for testing AI features)
- Basic understanding of intelligence analysis concepts

### First Time Setup

1. **Fork the Repository**
   ```bash
   # Visit https://github.com/yourusername/intellireport and click "Fork"
   git clone https://github.com/YOUR_USERNAME/intellireport.git
   cd intellireport
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install development dependencies
   pip install -e ".[dev]"
   ```

3. **Configure Environment**
   ```bash
   # Copy example environment file
   cp .env.example .env

   # Add your API keys
   echo "ANTHROPIC_API_KEY=your-key-here" >> .env
   ```

4. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   pytest tests/ -v

   # Run basic example
   python examples/basic_usage.py
   ```

## 💻 Development Environment

### Recommended Tools

- **IDE**: VS Code with Python extension
- **Code Formatting**: Black, isort
- **Linting**: flake8, mypy
- **Testing**: pytest, pytest-cov
- **Pre-commit**: Automated code quality checks

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📝 Contributing Guidelines

### What We're Looking For

- 🐛 **Bug fixes** with clear reproduction steps
- ✨ **New features** that enhance intelligence analysis capabilities
- 📚 **Documentation improvements** for better user experience
- 🧪 **Test improvements** to increase code coverage
- 🔧 **Performance optimizations** for better scalability

### What We're Not Looking For

- Breaking changes without discussion
- Features that don't align with intelligence analysis use cases
- Code without appropriate tests
- Large refactoring without prior discussion

## 🔄 Types of Contributions

### 1. Adding New Schemas

When adding support for new report types:

```python
# intellireport/schemas.py

class CustomReport(BaseModel):
    \"\"\"Custom report schema for specific use case.\"\"\"

    # Required fields
    title: str = Field(..., min_length=1, description="Report title")
    content: str = Field(..., min_length=10, description="Main content")

    # Optional fields with defaults
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    tags: List[str] = Field(default_factory=list)

    # Validation
    @validator('content')
    def validate_content(cls, v):
        if len(v.split()) < 5:
            raise ValueError('Content must have at least 5 words')
        return v
```

**Requirements for new schemas:**
- Comprehensive docstrings
- Input validation with clear error messages
- Default values for optional fields
- Unit tests covering all validation rules
- Example usage in documentation

### 2. Improving Extraction Capabilities

When enhancing extraction algorithms:

```python
# intellireport/extractors.py

class NewExtractor(BaseExtractor):
    \"\"\"Extractor for specialized intelligence analysis.\"\"\"

    def extract(self, text: str, **kwargs) -> Tuple[ExtractedData, int]:
        \"\"\"Extract specialized information from text.

        Args:
            text: Input text to process
            **kwargs: Additional configuration options

        Returns:
            Tuple of (extracted_data, tokens_used)

        Raises:
            ExtractionError: If extraction fails
        \"\"\"
        try:
            # Implementation with fallback mechanisms
            return self._extract_with_ai(text) or self._extract_with_patterns(text)
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise ExtractionError(f"Failed to extract data: {e}")
```

**Requirements for extraction improvements:**
- Fallback mechanisms for when AI fails
- Comprehensive error handling and logging
- Performance benchmarks vs. existing methods
- Support for multiple languages (if applicable)
- Integration tests with real-world data

### 3. Testing Requirements

All contributions must include comprehensive tests:

```python
# tests/test_new_feature.py

import pytest
from intellireport import ReportProcessor
from intellireport.schemas import ToneType


class TestNewFeature:
    \"\"\"Tests for new feature functionality.\"\"\"

    @pytest.fixture
    def processor(self):
        \"\"\"Create processor instance for testing.\"\"\"
        return ReportProcessor(api_key="test-key")

    def test_basic_functionality(self, processor):
        \"\"\"Test basic feature operation.\"\"\"
        # Arrange
        input_text = "Sample report text for testing"

        # Act
        result = processor.process(input_text)

        # Assert
        assert result.success
        assert result.data is not None
        assert len(result.errors) == 0

    def test_error_handling(self, processor):
        \"\"\"Test error conditions are handled gracefully.\"\"\"
        # Test invalid input
        with pytest.raises(ValueError):
            processor.process("")

    @pytest.mark.parametrize("tone,expected", [
        (ToneType.NGO, "humanitarian"),
        (ToneType.CORPORATE, "business"),
        (ToneType.PROFESSIONAL, "intelligence")
    ])
    def test_tone_variations(self, processor, tone, expected):
        \"\"\"Test behavior across different tones.\"\"\"
        result = processor.process("Test text", tone=tone)
        assert expected in result.data.standard_report.bluf.lower()
```

**Testing Standards:**
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-end Tests**: Test complete workflows
- **Performance Tests**: Verify acceptable performance
- **Error Handling**: Test all error conditions

### 4. Code Style Guide

#### Python Style

Follow PEP 8 with these specific guidelines:

```python
# Good: Clear, descriptive names
def extract_bottom_line_up_front(text: str) -> str:
    \"\"\"Extract BLUF from intelligence report text.\"\"\"
    pass

# Good: Type hints for all public functions
def process_report(
    text: str,
    tone: ToneType = ToneType.PROFESSIONAL,
    extract_entities: bool = True
) -> ProcessingResult:
    \"\"\"Process intelligence report with specified parameters.\"\"\"
    pass

# Good: Comprehensive docstrings
class ReportProcessor:
    \"\"\"Main class for processing intelligence reports.

    This class provides methods for extracting structured information
    from unstructured intelligence reports using AI-powered analysis.

    Attributes:
        api_key: Anthropic API key for AI processing
        tone: Default tone for analysis
        max_retries: Maximum retry attempts for API calls

    Example:
        >>> processor = ReportProcessor()
        >>> result = processor.process("Security incident report...")
        >>> print(result.data.standard_report.bluf)
    \"\"\"
```

#### Import Organization

```python
# Standard library imports
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Union

# Third-party imports
import anthropic
import pydantic
from pydantic import BaseModel, Field

# Local imports
from .schemas import StandardReport, ToneType
from .extractors import BLUFExtractor
from .utils import setup_logging
```

#### Error Handling

```python
# Good: Specific exception types
class IntelliReportError(Exception):
    \"\"\"Base exception for IntelliReport errors.\"\"\"
    pass

class ExtractionError(IntelliReportError):
    \"\"\"Raised when extraction fails.\"\"\"
    pass

class ValidationError(IntelliReportError):
    \"\"\"Raised when data validation fails.\"\"\"
    pass

# Good: Comprehensive error handling
def process_text(text: str) -> StandardReport:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    try:
        result = extract_report_data(text)
        return validate_report(result)
    except APIError as e:
        logger.error(f"API call failed: {e}")
        raise ExtractionError(f"Failed to process text: {e}")
    except ValidationError:
        # Re-raise validation errors as-is
        raise
    except Exception as e:
        logger.exception("Unexpected error in process_text")
        raise IntelliReportError(f"Unexpected error: {e}")
```

## 🧪 Testing Requirements

### Test Coverage

Maintain at least 85% test coverage for all new code:

```bash
# Run tests with coverage
pytest --cov=intellireport tests/

# Generate HTML coverage report
pytest --cov=intellireport --cov-report=html tests/
```

### Test Categories

1. **Unit Tests** (`tests/unit/`)
   - Test individual functions
   - Mock external dependencies
   - Fast execution (<1s per test)

2. **Integration Tests** (`tests/integration/`)
   - Test component interactions
   - Use test data, not live APIs
   - Moderate execution time

3. **End-to-End Tests** (`tests/e2e/`)
   - Test complete workflows
   - May use live APIs (with test keys)
   - Slower execution acceptable

### Test Data

Store test data in `tests/fixtures/`:

```bash
tests/fixtures/
├── sample_reports/
│   ├── security_incident.txt
│   ├── humanitarian_report.txt
│   └── intelligence_brief.txt
├── expected_outputs/
│   └── processed_reports.json
└── mock_responses/
    └── anthropic_responses.json
```

## 📚 Documentation

### Docstring Standards

Use Google-style docstrings:

```python
def process_batch(
    self,
    texts: List[str],
    batch_size: int = 5,
    **kwargs
) -> List[ProcessingResult]:
    \"\"\"Process multiple reports in batches.

    Args:
        texts: List of report texts to process
        batch_size: Number of reports to process simultaneously
        **kwargs: Additional arguments passed to process()

    Returns:
        List of ProcessingResult objects, one per input text

    Raises:
        ValueError: If texts is empty or batch_size < 1
        ExtractionError: If batch processing fails

    Example:
        >>> processor = ReportProcessor()
        >>> reports = ["Report 1", "Report 2", "Report 3"]
        >>> results = processor.process_batch(reports, batch_size=2)
        >>> for result in results:
        ...     print(result.data.standard_report.bluf)
    \"\"\"
```

### README Updates

When adding new features, update the README.md:

1. Add to feature list
2. Include code example
3. Update API documentation section
4. Add to use cases if applicable

### API Documentation

For significant API changes, update the documentation:

```python
# Add type hints for IDE support
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anthropic import Anthropic
```

## 🔄 Development Workflow

### 1. Planning Phase

Before starting work:

1. **Check existing issues** - avoid duplicate work
2. **Create/comment on issue** - discuss approach
3. **Get feedback** - ensure alignment with project goals

### 2. Implementation Phase

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes iteratively
git add .
git commit -m "Add: initial implementation of feature X"

# Keep commits small and focused
git commit -m "Fix: handle edge case in extraction"
git commit -m "Test: add unit tests for new feature"
git commit -m "Docs: update API documentation"
```

### 3. Testing Phase

```bash
# Run full test suite
pytest tests/ -v

# Check code coverage
pytest --cov=intellireport tests/

# Run performance tests
pytest tests/performance/ -v

# Test documentation examples
python -m doctest README.md
```

### 4. Code Quality

```bash
# Format code
black intellireport/
isort intellireport/

# Lint code
flake8 intellireport/
mypy intellireport/

# Run pre-commit hooks
pre-commit run --all-files
```

## 📤 Submitting Changes

### Pull Request Process

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Use the PR template
   - Link related issues
   - Include screenshots for UI changes
   - Add detailed description of changes

3. **PR Review Process**
   - Automated checks must pass
   - At least one reviewer approval required
   - Address all review feedback
   - Maintain clean commit history

### PR Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
```

### Commit Message Format

Follow conventional commits:

```bash
# Format: type(scope): description
feat(extractor): add support for multi-language extraction
fix(redactor): handle edge case in PII detection
docs(api): update ReportProcessor documentation
test(core): add integration tests for batch processing
perf(extract): optimize entity extraction algorithm
```

## 🚀 Release Process

### Version Numbering

Follow Semantic Versioning (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

For maintainers preparing releases:

1. **Update Version**
   ```bash
   # Update version in setup.py, __init__.py
   git commit -m "chore: bump version to X.Y.Z"
   ```

2. **Update Changelog**
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD
   ### Added
   - New feature descriptions
   ### Changed
   - Modified feature descriptions
   ### Fixed
   - Bug fix descriptions
   ```

3. **Create Release**
   ```bash
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin vX.Y.Z
   ```

4. **Build and Deploy**
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## 🎯 Contribution Recognition

### Contributors

All contributors are recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for significant contributions

### Hall of Fame

Outstanding contributors may be featured in:
- Project documentation
- Conference presentations
- IJEOMA Safety Platform showcases

## 🤝 Community

### Getting Help

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Email**: [dev@ijeoma.safety](mailto:dev@ijeoma.safety) for private matters
- **Discord**: [IJEOMA Safety Community](https://discord.gg/ijeoma) (coming soon)

### Regular Events

- **Monthly Community Calls**: First Friday of each month
- **Quarterly Roadmap Reviews**: Discuss upcoming features
- **Annual Contributors Summit**: Virtual gathering of contributors

---

## 🙏 Thank You

Your contributions help make intelligence analysis more accessible and effective for organizations worldwide. Together, we're building tools that support humanitarian response, corporate security, and government intelligence operations.

**Happy coding! 🚀**

---

*This contributing guide is part of the IJEOMA Safety Platform documentation. For questions about this guide, please open an issue or contact [dev@ijeoma.safety](mailto:dev@ijeoma.safety).*