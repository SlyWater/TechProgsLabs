import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent
APPSETTINGS_PATH = BASE_DIR / "appsettings.json"


@dataclass(frozen=True)
class Settings:
    database_url: str

    @property
    def sqlite_file_path(self) -> Path | None:
        parsed = urlparse(self.database_url)
        if parsed.scheme != "sqlite":
            return None

        raw_path = parsed.path
        if raw_path.startswith("/"):
            raw_path = raw_path[1:]

        path = Path(raw_path)
        if not path.is_absolute():
            path = (BASE_DIR / path).resolve()

        return path


@lru_cache
def get_settings() -> Settings:
    if APPSETTINGS_PATH.exists():
        config = json.loads(APPSETTINGS_PATH.read_text(encoding="utf-8"))
    else:
        config = {}

    database_url = config.get("DataBaseUrl", "sqlite:///./data/shop.db")
    settings = Settings(database_url=database_url)

    sqlite_file_path = settings.sqlite_file_path
    if sqlite_file_path is not None:
        sqlite_file_path.parent.mkdir(parents=True, exist_ok=True)

    return settings
