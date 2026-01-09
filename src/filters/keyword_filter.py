from src.models import ConfigModel, TweetModel
from src.utils import get_logger

logger = get_logger("FilterEngine")


class FilterEngine:
    def __init__(self, config: ConfigModel):
        self.config = config

    def process(self, tweet: TweetModel) -> TweetModel | None:
        if not self.config.topics:
            return tweet

        matched_keywords = set()
        matched_topics = set()
        text_lower = tweet.text.lower()

        for topic, keywords in self.config.topics.items():
            if not keywords:
                continue
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched_keywords.add(kw)
                    matched_topics.add(topic)

        if not matched_keywords:
            return None

        tweet.matching_keywords = list(matched_keywords)
        tweet.matching_topics = list(matched_topics)

        return tweet
