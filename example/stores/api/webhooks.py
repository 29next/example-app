import hmac
import hashlib

from django.conf import settings


def webhook_payload_validator(payload, signature):
    expected_sig = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        payload.encode(), hashlib.sha256
    ).hexdigest()
    return True if expected_sig == signature else False

