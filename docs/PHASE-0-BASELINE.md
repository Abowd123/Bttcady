# Phase 0 — Baseline and recovery preparation

## Completed
- Created an isolated repair workspace at `/data/bot-repair`.
- Preserved the original uploaded archive under `backups/original-upload.zip`.
- Removed generated Python bytecode from the repair copy.
- Added `.gitignore` rules for tokens, sessions, databases, media, logs, and backups.
- Added `.env.example` containing names only, with no secret values.
- Added a legacy `information.py.example` without credentials.
- Created placeholders for documentation and tests.
- Initialized a local Git repository without committing the unsafe source snapshot.

## Baseline
- Python source files: 31
- Approximate Python lines: 23,901
- Pyrogram handlers: 69
- Redis calls found statically: 3,037
- Broad exception handlers found statically: 137
- Syntax compilation: passed

## Current components
- Telegram framework: Pyrogram 2.0.97
- State: synchronous Redis client
- Local data: kvsqlite/SQLite
- Media: ffmpeg, yt-dlp, pytube, pydub, gTTS, Shazam
- External HTTP: requests, httpx, aiohttp

## Deployment blockers found
- Source contains active credentials and privileged hard-coded user IDs.
- README refers to a missing `start.sh`.
- `Run` refers to missing `r3d.txt` and contains an install typo.
- `getids` is imported while commented out in requirements.
- Production startup has not been attempted to avoid using exposed credentials.

## Before production
1. Revoke and replace the bot token and any exposed Telegram session/API credentials.
2. Remove hard-coded privileged IDs and remote code/system command execution.
3. Move configuration to environment variables.
4. Only then create the first safe Git commit.
