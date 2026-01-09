import logging
import sys


class LoggerSetup:
    @staticmethod
    def setup_logging(debug: bool = False) -> logging.Logger:
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        return logging.getLogger("TweetScraper")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
