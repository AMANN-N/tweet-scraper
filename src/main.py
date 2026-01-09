import argparse
import os
import sys

from dotenv import load_dotenv

from src.api.twitter_client import TwitterClient
from src.core.config import load_config, validate_env_vars
from src.core.exceptions import TweetScraperError
from src.filters import FilterEngine
from src.models import TweetModel
from src.output import MarkdownWriter
from src.utils import LoggerSetup, parse_iso8601


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and archive Tweets to Markdown."
    )
    parser.add_argument(
        "--config", type=str, default="config/config.yaml", help="Path to config file"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Fetch and filter but do not save"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logger = LoggerSetup.setup_logging(args.verbose)

    try:
        load_dotenv()
        validate_env_vars()

        config = load_config(args.config)
        logger.info(f"Loaded config for target user: {config.target_username}")

        bearer_token = os.getenv("X_BEARER_TOKEN")
        assert bearer_token is not None
        twitter = TwitterClient(bearer_token)
        filter_engine = FilterEngine(config)
        markdown_writer = MarkdownWriter(config.output_file)

        if not args.dry_run:
            markdown_writer.ensure_output_dir()

        user_id = twitter.get_user_id(config.target_username)
        if not user_id:
            logger.error("Could not resolve user ID. Exiting.")
            sys.exit(1)
        logger.info(f"Resolved {config.target_username} to ID: {user_id}")

        total_fetched = 0
        total_passed = 0
        total_archived = 0

        for page in twitter.fetch_tweets(user_id, config):
            logger.info(f"Processing page with {len(page)} tweets...")
            total_fetched += len(page)

            for tweet_data in page:
                metrics = tweet_data.get("public_metrics", {})
                media_urls = tweet_data.get("media_urls", [])

                tweet_model = TweetModel(
                    tweet_id=tweet_data["id"],
                    author_username=config.target_username.strip("@"),
                    created_at=parse_iso8601(tweet_data["created_at"]),
                    text=tweet_data["text"],
                    permalink=f"https://twitter.com/{config.target_username.strip('@')}/status/{tweet_data['id']}",
                    like_count=metrics.get("like_count", 0),
                    retweet_count=metrics.get("retweet_count", 0),
                    reply_count=metrics.get("reply_count", 0),
                    quote_count=metrics.get("quote_count", 0),
                    in_reply_to_status_id=(
                        tweet_data.get("referenced_tweets", [{}])[0].get("id")
                        if "referenced_tweets" in tweet_data
                        else None
                    ),
                    media_urls=media_urls,
                )

                filtered_tweet = filter_engine.process(tweet_model)
                if not filtered_tweet:
                    continue

                total_passed += 1

                if args.dry_run:
                    logger.info(
                        f"[DRY RUN] Would save: {filtered_tweet.text[:50]}... (Media: {len(filtered_tweet.media_urls)})"
                    )
                    continue

                markdown_writer.append_tweet(filtered_tweet)
                total_archived += 1

    except TweetScraperError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

    logger.info("=" * 30)
    logger.info("SUMMARY")
    logger.info(f"Fetched: {total_fetched}")
    logger.info(f"Passed Filters: {total_passed}")
    logger.info(f"Saved to {config.output_file}: {total_archived}")
    logger.info("=" * 30)


if __name__ == "__main__":
    main()
