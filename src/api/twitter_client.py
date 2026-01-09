import time
from collections.abc import Generator
from typing import Any

import requests

from src.core.constants import BASE_URL, DEFAULT_MAX_RESULTS, USER_AGENT
from src.core.exceptions import APIError, RateLimitError, UserNotFoundError
from src.models import ConfigModel
from src.utils import get_logger

logger = get_logger("TwitterClient")


class TwitterClient:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "User-Agent": USER_AGENT,
        }

    def _make_request(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                json_data = response.json()
                assert isinstance(json_data, dict)
                return json_data

            if response.status_code == 429:
                reset_time = int(response.headers.get("x-rate-limit-reset", 0))
                current_time = int(time.time())
                sleep_seconds = max(reset_time - current_time, 0) + 1
                logger.warning(f"Rate limit hit! Sleeping for {sleep_seconds} seconds...")
                time.sleep(sleep_seconds)
                retry_count += 1
                continue

            if response.status_code == 404:
                raise UserNotFoundError(f"Resource not found: {response.text}")

            logger.error(f"Twitter API Error: {response.status_code} - {response.text}")
            raise APIError(f"API request failed: {response.status_code}")

        raise RateLimitError(f"Max retries exceeded for URL: {url}")

    def get_user_id(self, username: str) -> str | None:
        clean_username = username.lstrip("@")
        url = f"{self.base_url}/users/by/username/{clean_username}"
        try:
            data = self._make_request(url, params={})
            if "data" in data:
                user_id = data["data"]["id"]
                assert isinstance(user_id, str)
                return user_id
            raise UserNotFoundError(f"User not found: {username}")
        except (APIError, UserNotFoundError) as e:
            logger.error(f"Failed to resolve user ID: {e}")
            raise

    def fetch_tweets(self, user_id: str, config: ConfigModel) -> Generator[list[dict[str, Any]]]:
        url = f"{self.base_url}/tweets/search/recent"

        query = f"from:{user_id}"
        if not config.search.include_replies:
            query += " -is:reply"
        if not config.search.include_retweets:
            query += " -is:retweet"

        params = {
            "query": query,
            "max_results": min(config.search.max_results, DEFAULT_MAX_RESULTS),
            "tweet.fields": "created_at,public_metrics,author_id,in_reply_to_user_id,referenced_tweets,text",
            "expansions": "author_id,attachments.media_keys",
            "media.fields": "url,preview_image_url,type",
        }

        if config.search.start_time:
            params["start_time"] = config.search.start_time
        if config.search.end_time:
            params["end_time"] = config.search.end_time

        next_token = None

        while True:
            if next_token:
                params["next_token"] = next_token

            logger.info(
                f"Fetching page {len(params.get('next_token', 'initial'))} with params: query={query}, max_results={params.get('max_results')}"
            )
            json_response = self._make_request(url, params)

            tweets = json_response.get("data", [])
            includes = json_response.get("includes", {})
            media_map = {
                m["media_key"]: m.get("url") or m.get("preview_image_url")
                for m in includes.get("media", [])
            }

            for tweet in tweets:
                if "attachments" in tweet and "media_keys" in tweet["attachments"]:
                    tweet_media = []
                    for key in tweet["attachments"]["media_keys"]:
                        if key in media_map and media_map[key]:
                            tweet_media.append(media_map[key])
                    tweet["media_urls"] = tweet_media

            if not tweets:
                logger.info("No more tweets found.")
                break

            logger.info(f"Fetched {len(tweets)} tweets in this page")

            yield tweets

            next_token = json_response.get("meta", {}).get("next_token")
            if not next_token:
                break
