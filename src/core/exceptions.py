class TweetScraperError(Exception):
    """Base exception for tweet-scraper"""


class MissingConfigError(TweetScraperError):
    """Raised when required config is missing"""


class APIError(TweetScraperError):
    """Raised when API request fails"""


class RateLimitError(APIError):
    """Raised when rate limit is exceeded"""


class UserNotFoundError(APIError):
    """Raised when Twitter user not found"""


class NotionError(TweetScraperError):
    """Raised when Notion API fails"""
