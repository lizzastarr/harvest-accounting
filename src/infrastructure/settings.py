"""Читання appsettings.json."""
import json
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Settings:
    app_name: str
    storage_type: str
    storage_path: Optional[str]


def load_settings(path: str = "appsettings.json") -> Settings:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    storage = raw.get("storage", {})
    return Settings(raw.get("app_name", "Облік урожаю"),
                    storage.get("type", "memory"), storage.get("path"))
