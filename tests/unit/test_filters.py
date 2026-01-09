from datetime import datetime

from src.filters import FilterEngine
from src.models import ConfigModel, SearchConfig, TweetModel


def test_keyword_matching(filter_engine, mock_tweet):
    result = filter_engine.process(mock_tweet)
    assert result is not None
    assert "AI" in result.matching_topics
    assert "ai" in result.matching_keywords


def test_no_match(filter_engine):
    tweet = TweetModel(
        tweet_id="123",
        author_username="user",
        created_at=datetime.now(),
        text="This is about cooking",
        permalink="https://twitter.com/user/status/123",
    )
    result = filter_engine.process(tweet)
    assert result is None


def test_no_topics(mock_tweet):
    config = ConfigModel(
        target_username="@user", search=SearchConfig(), topics={}, output_file="test.md"
    )
    engine = FilterEngine(config)
    result = engine.process(mock_tweet)
    assert result is not None
