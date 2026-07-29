"""Secure bot entry point.

Configuration is read from environment variables; this module never writes
credentials or generated Python configuration files.
"""

import logging
import os
import re

import requests
from pyrogram import Client, idle

import config


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("bot")


def find_urls(text: str | None) -> list[str]:
    if not text:
        return []
    pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    return [match[0] for match in re.findall(pattern, text)]


def load_bot_username() -> str:
    if config.botUsername:
        return config.botUsername
    response = requests.get(
        "https://api.telegram.org/bot" + config.token + "/getMe",
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError("Telegram getMe rejected the configured bot token")
    return payload["result"]["username"]


def prepare_runtime_state() -> None:
    config.r.ping()
    config.r.set(f"{config.Dev_Zaid}botowner", config.sudo_id)
    config.r.setnx(f"{config.Dev_Zaid}:botkey", "⇜")
    config.r.setnx(f"{config.Dev_Zaid}:BotName", "رعد")
    config.r.setnx(f"{config.Dev_Zaid}:BotChannel", "eFFb0t")


def main() -> None:
    prepare_runtime_state()
    config.botUsername = load_bot_username()

    app = Client(
        f"{config.Dev_Zaid}r3d",
        api_id=config.api_id,
        api_hash=config.api_hash,
        bot_token=config.token,
        plugins={"root": "Plugins"},
        workers=config.BOT_WORKERS,
    )

    app.start()
    logger.info(
        "Bot started as @%s version=%s workers=%s",
        config.botUsername,
        config.BOT_VERSION,
        config.BOT_WORKERS,
    )

    developer_group = config.r.get(f"DevGroup:{config.Dev_Zaid}")
    if developer_group:
        try:
            app.send_message(int(developer_group), "تم تشغيل البوت بنجاح ✔️")
        except Exception:
            logger.exception("Could not send startup notification")

    try:
        idle()
    finally:
        app.stop()
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()
