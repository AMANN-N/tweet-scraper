import os

from src.models import TweetModel
from src.utils import get_logger

logger = get_logger("MarkdownWriter")


class MarkdownWriter:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def ensure_output_dir(self) -> None:
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

    def append_tweet(self, tweet: TweetModel) -> None:
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(
                f"## [{tweet.created_at.strftime('%Y-%m-%d %H:%M')}]({tweet.permalink})\n\n"
            )
            f.write(f"{tweet.text}\n\n")

            for media_url in tweet.media_urls:
                f.write(f"![Media]({media_url})\n\n")

            f.write("---\n\n")

        logger.debug(f"Appended tweet {tweet.tweet_id} to {self.output_file}")
