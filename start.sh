#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

required=(BOT_TOKEN API_ID API_HASH OWNER_ID)
for name in "${required[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: $name" >&2
    exit 1
  fi
done

command -v ffmpeg >/dev/null 2>&1 || {
  echo "ffmpeg is required but was not found" >&2
  exit 1
}

exec python3 main.py
