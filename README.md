# Tweet to Markdown Scraper

A Python tool to fetch tweets from a specific X (Twitter) user, optionally filter them, and save them to a clean Markdown file.

## Features

- **Official API Only**: Uses X API v2 (Recent Search)
- **Media Support**: Automatically fetches and embeds images/media
- **Configurable**:
  - Fetch all tweets or filter by keywords
  - Customizable output file path
- **Rich Data**: Output includes timestamp, permalink, text, and media
- **Modern Stack**: Python 3.13+, Pydantic v2, Type hints

## Requirements

- Python 3.13+
- X (Twitter) API credentials (Bearer Token)

## Installation

### Basic Installation

```bash
# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Development Installation

```bash
# Install with dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Configuration

### 1. Copy Example Files

```bash
cp .env.example .env
cp config/config.example.yaml config/config.yaml
```

### 2. Edit `.env`

```env
X_BEARER_TOKEN=your_token_here
```

### 3. Edit `config/config.yaml`

- Set `target_username` to the Twitter user
- Configure `topics` for keyword filtering (leave empty for all tweets)
- Set `output_file` to your desired save location

## Usage

### Export to Markdown

```bash
python3 -m src.main --config config/config.yaml
```

### Dry Run (Test Filters)

```bash
python3 -m src.main --dry-run
```

### Verbose Logging

```bash
python3 -m src.main --verbose
```

## Development

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black src tests

# Lint
ruff check src tests --fix

# Type check
mypy src
```

## License

MIT
