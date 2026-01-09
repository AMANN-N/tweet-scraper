from datetime import datetime

import pytest

from src.filters import FilterEngine
from src.models import ConfigModel, SearchConfig, TweetModel


@pytest.fixture
def mock_config():
    return ConfigModel(
        target_username="@testuser",
        search=SearchConfig(),
        topics={"AI": ["ai", "machine learning"]},
        output_file="test_output.md",
    )


@pytest.fixture
def mock_tweet():
    return TweetModel(
        tweet_id="1234567890",
        author_username="testuser",
        created_at=datetime.now(),
        text="This is a tweet about AI and machine learning",
        permalink="https://twitter.com/testuser/status/1234567890",
        like_count=10,
        retweet_count=5,
        reply_count=2,
        quote_count=1,
    )


@pytest.fixture
def filter_engine(mock_config):
    return FilterEngine(mock_config)


@pytest.fixture
def temp_output_file(tmp_path):
    return str(tmp_path / "test_tweets.md")
