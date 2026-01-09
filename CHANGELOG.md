# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-09

### Added
- Notion integration with `--output-notion` CLI flag
- Test infrastructure with pytest and coverage
- Code quality tooling (Black, Ruff, MyPy, pre-commit)
- Modular package structure with separated concerns
- Type hints throughout the codebase
- Custom exceptions for better error handling
- Comprehensive documentation (README, CONTRIBUTING)

### Changed
- Refactored into proper Python package structure
- Updated to Python 3.13
- Moved API client to `src/api/` module
- Separated models into `src/models/`
- Extracted config loading to `src/core/config.py`
- Extracted output writing to `src/output/`
- Split utils into `logging.py` and `date_utils.py`

### Fixed
- Better error handling with custom exceptions
- Improved rate limit handling in TwitterClient

## [0.1.0] - 2024-12-07

### Added
- Initial release
- Twitter/X API v2 integration
- Markdown export
- Keyword filtering
- Date range filtering
- Dry-run mode
- Verbose logging
