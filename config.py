"""Runtime configuration loaded only from environment variables."""

import os
from pathlib import Path

import redis
from kvsqlite.sync import Client as DB


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _required_int(name: str) -> int:
    value = _required(name)
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer") from exc


token = _required("BOT_TOKEN")
api_id = _required_int("API_ID")
api_hash = _required("API_HASH")
sudo_id = _required_int("OWNER_ID")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0").strip()
botUsername = os.getenv("BOT_USERNAME", "").strip().lstrip("@")
ARQ_API_KEY = os.getenv("ARQ_API_KEY", "").strip()
ARQ_API_URL = os.getenv("ARQ_API_URL", "https://arq.hamker.dev").strip()
BOT_VERSION = os.getenv("BOT_VERSION", "0.5.0-router-foundation").strip()
BOT_WORKERS = max(4, min(64, int(os.getenv("BOT_WORKERS", "16"))))
Dev_Zaid = token.split(":", 1)[0]

r = redis.Redis.from_url(redis_url, decode_responses=True)

_data_dir = Path(os.getenv("DATA_DIR", ".")).resolve()
_data_dir.mkdir(parents=True, exist_ok=True)
ytdb = DB(str(_data_dir / "ytdb.sqlite"))
sounddb = DB(str(_data_dir / "sounddb.sqlite"))
wsdb = DB(str(_data_dir / "wsdb.sqlite"))
