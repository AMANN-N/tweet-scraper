# Contributing to Tweet Scraper

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python3.13 -m venv venv`
3. Activate the venv
4. Install dev dependencies: `pip install -r requirements-dev.txt`
5. Install pre-commit hooks: `pre-commit install`

## Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

## Code Style

This project uses:

- **Black** for formatting
- **Ruff** for linting
- **MyPy** for type checking

Run all quality checks:

```bash
black src tests
ruff check src tests --fix
mypy src
```

## Submitting Changes

1. Create a feature branch
2. Make your changes
3. Run tests and quality checks
4. Submit a pull request with a clear description
