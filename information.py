"""Deprecated configuration module.

Real credentials must be supplied through environment variables. This file is
kept temporarily so old imports fail safely instead of exposing secrets.
"""

raise RuntimeError(
    "information.py is no longer used; configure BOT_TOKEN and OWNER_ID in the environment"
)
