from pydantic import BaseModel

from src.models.tweet import SearchConfig


class ConfigModel(BaseModel):
    target_username: str
    search: SearchConfig
    topics: dict[str, list[str]] = {}
    output_file: str = "tweets.md"
