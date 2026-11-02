import base64
import binascii
import hmac
import os
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY_ENV_VAR = "APP_ACCESS_KEY"


def _is_valid_base64(value: str) -> bool:
    try:
        base64.b64decode(value, validate=True)
        return True
    except (binascii.Error, ValueError):
        return False


def validate_access_key(provided_key: str) -> Tuple[bool, str]:
    """
    Validates the application access key against APP_ACCESS_KEY (base64 string).
    Fails closed: if no server key is configured, access is denied.
    """
    expected = (os.getenv(ACCESS_KEY_ENV_VAR) or "").strip()
    if not expected:
        return False, f"Server access key is not configured. Set {ACCESS_KEY_ENV_VAR} in the environment."

    provided = (provided_key or "").strip()
    if not provided:
        return False, "Access key is required to proceed."

    if not _is_valid_base64(provided):
        return False, "Invalid access key."

    if not hmac.compare_digest(provided.encode("utf-8"), expected.encode("utf-8")):
        return False, "Invalid access key."

    return True, ""
