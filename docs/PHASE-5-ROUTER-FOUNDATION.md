# Phase 5 — Router foundation after static inspection

## Completed
- Created a stable real workspace instead of editing through the extraction symlink.
- Added shared per-message text normalization with a five-second cache.
- Bot-name stripping and local/global custom-command aliases are now resolved once per message.
- Added early command gates to promote, demote, rank-list, and rank-clear handlers.
- Ordinary messages now leave those rank handlers before their repeated permission and Redis checks.
- Removed all remaining manual `Thread(target=...)` calls again in the stable workspace.
- Added a bounded Pyrogram worker count through `BOT_WORKERS` (default 16).
- Removed the remaining inherited privileged account from the rank helper.
- Added regression tests for routing, bounded workers, manual threads, and the privileged ID.

## Next router batches
- Moderation and group settings.
- Games and entertainment commands.
- Custom commands/replies, which require preserving interactive state.
- Downloader routing and a dedicated bounded media queue.
