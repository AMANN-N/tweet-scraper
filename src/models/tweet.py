from datetime import datetime

from pydantic import BaseModel


class TweetModel(BaseModel):
    tweet_id: str
    author_username: str
    created_at: datetime
    text: str
    permalink: str
    like_count: int = 0
    retweet_count: int = 0
    reply_count: int = 0
    quote_count: int = 0
    in_reply_to_status_id: str | None = None
    matching_keywords: list[str] = []
    matching_topics: list[str] = []
    media_urls: list[str] = []


class SearchConfig(BaseModel):
    include_replies: bool = False
    include_retweets: bool = False
    max_results: int = 10
    start_time: str | None = None
    end_time: str | None = None
