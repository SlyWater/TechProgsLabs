import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
APPSETTINGS_PATH = BASE_DIR / "appsettings.json"


@dataclass(frozen=True)
class Settings:
    database_file_path: Path


@lru_cache
def get_settings() -> Settings:
    if APPSETTINGS_PATH.exists():
        config = json.loads(APPSETTINGS_PATH.read_text(encoding="utf-8"))
    else:
        config = {}

    file_path = config.get("DataBaseFilePath", "database.json")
    return Settings(database_file_path=(BASE_DIR / file_path).resolve())
