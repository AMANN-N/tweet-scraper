from unittest.mock import Mock, patch

import pytest

from src.api.twitter_client import TwitterClient
from src.core.exceptions import UserNotFoundError


@pytest.fixture
def twitter_client():
    return TwitterClient("test_bearer_token")


def test_get_user_id_not_found(twitter_client, monkeypatch):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with pytest.raises(UserNotFoundError):
            twitter_client.get_user_id("nonexistentuser12345")
