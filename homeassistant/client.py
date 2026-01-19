import os
from contextvars import ContextVar
from typing import Any

from requests import get, post

# Context variable for per-request token (used by API)
# Falls back to env var for CLI usage
_token_context: ContextVar[str | None] = ContextVar("ha_token", default=None)

URL = os.getenv("HOMEASSISTANT_URL", "http://homeassistant.local:8123") + "/api"


def set_token(token: str):
    """Set the token for the current request context."""
    _token_context.set(token)


def get_token() -> str | None:
    """Get token from context or fall back to env var."""
    return _token_context.get() or os.getenv("HOMEASSISTANT_TOKEN")


def get_entity_status(entity_id: str) -> dict[str, Any]:
    token = get_token()
    if not token:
        raise ValueError("No Home Assistant token provided")

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{URL}/states/{entity_id}"

    response = get(url, headers=headers)

    resp = response.json()

    return resp


def command_service(
    service: str, homeassistant_commandstr: str, data: dict
) -> dict[str, Any]:
    token = get_token()
    if not token:
        raise ValueError("No Home Assistant token provided")

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{URL}/services/{service}/{homeassistant_commandstr}"

    response = post(url, headers=headers, json=data)

    resp = response.json()

    return resp
