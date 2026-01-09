from datetime import datetime

from src.models import ConfigModel, SearchConfig, TweetModel


def test_tweet_model():
    tweet = TweetModel(
        tweet_id="123",
        author_username="user",
        created_at=datetime.now(),
        text="test",
        permalink="https://twitter.com/user/status/123",
    )
    assert tweet.tweet_id == "123"
    assert tweet.like_count == 0


def test_config_model():
    config = ConfigModel(target_username="@user", search=SearchConfig())
    assert config.target_username == "@user"
    assert config.topics == {}
