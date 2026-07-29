"""Shared, short-lived message text normalization for legacy handlers.

Multiple plugins used to repeat the same bot-name and custom-command Redis
lookups for every group message. This cache performs that normalization once
per message and shares the result across routed handlers.
"""

from __future__ import annotations

from threading import Lock
import time

from config import Dev_Zaid, r


_MESSAGE_TTL = 5.0
_IDENTITY_TTL = 15.0
_lock = Lock()
_message_cache: dict[tuple[int, int], tuple[float, str]] = {}
_identity_cache: tuple[float, str] | None = None


def _bot_name() -> str:
    global _identity_cache
    now = time.monotonic()
    with _lock:
        if _identity_cache and now - _identity_cache[0] <= _IDENTITY_TTL:
            return _identity_cache[1]

    name = r.get(f"{Dev_Zaid}:BotName") or "رعد"
    with _lock:
        _identity_cache = (now, str(name))
    return str(name)


def normalize_message_text(message) -> str:
    raw = (getattr(message, "text", None) or "").strip()
    if not raw:
        return ""

    chat = getattr(message, "chat", None)
    chat_id = int(getattr(chat, "id", 0) or 0)
    message_id = int(getattr(message, "id", 0) or 0)
    cache_key = (chat_id, message_id)
    now = time.monotonic()

    with _lock:
        cached = _message_cache.get(cache_key)
        if cached and now - cached[0] <= _MESSAGE_TTL:
            return cached[1]

    text = raw
    name = _bot_name()
    prefix = name + " "
    if text.startswith(prefix):
        text = text[len(prefix):]

    pipe = r.pipeline(transaction=False)
    pipe.get(f"{chat_id}:Custom:{chat_id}{Dev_Zaid}&text={text}")
    pipe.get(f"Custom:{Dev_Zaid}&text={text}")
    local_alias, global_alias = pipe.execute()
    normalized = str(local_alias or global_alias or text)

    with _lock:
        _message_cache[cache_key] = (now, normalized)
        if len(_message_cache) > 10_000:
            cutoff = now - _MESSAGE_TTL
            for key, (created, _) in list(_message_cache.items()):
                if created < cutoff:
                    _message_cache.pop(key, None)
    return normalized


def matches_command(text: str, exact: frozenset[str], prefixes: tuple[str, ...]) -> bool:
    return text in exact or text.startswith(prefixes)


def clear_message_context_cache() -> None:
    global _identity_cache
    with _lock:
        _message_cache.clear()
        _identity_cache = None
