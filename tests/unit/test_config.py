import pytest

from src.core.config import validate_env_vars
from src.core.exceptions import MissingConfigError


def test_validate_env_vars_missing(monkeypatch):
    monkeypatch.delenv("X_BEARER_TOKEN", raising=False)
    with pytest.raises(MissingConfigError):
        validate_env_vars()


def test_validate_env_vars_present(monkeypatch, mock_config):
    monkeypatch.setenv("X_BEARER_TOKEN", "test_token")
    validate_env_vars()
