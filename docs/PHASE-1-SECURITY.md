# Phase 1 — Security hardening

## Completed in source
- Replaced file-based credentials with required environment variables.
- Removed the embedded Telegram API credentials and the commented user session.
- Stopped `main.py` from generating or rewriting `config.py` and `information.py`.
- Replaced inherited hard-coded privileged user IDs with the configured owner ID.
- Removed Telegram handlers for remote Python evaluation, shell commands, expression evaluation, and remote code execution.
- Disabled the plugin that edited Python source files through Telegram.
- Added fail-fast validation for missing configuration.
- Added a timeout and status validation to Telegram `getMe` startup lookup.
- Corrected the default bot name/channel Redis keys.

## Required outside the source
- Revoke the old token in BotFather and create a new one.
- Revoke the exposed user session, if it was ever active.
- Replace the exposed Telegram API credentials if they belong to this deployment.
- Supply the new values through the process environment; do not send them in chat or commit them.

## Environment variables
- `BOT_TOKEN`
- `API_ID`
- `API_HASH`
- `OWNER_ID`
- `REDIS_URL`
- Optional: `BOT_USERNAME`, `DATA_DIR`, `LOG_LEVEL`
