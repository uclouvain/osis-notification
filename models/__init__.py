try:
    from .notifications import (
        EMAIL_TYPE,
        Notification,
        PENDING_STATE,
        READ_STATE,
        SENT_STATE,
        WebNotification,
        WEB_TYPE,
    )
except RuntimeError as e:  # pragma: no cover
    # There's a weird bug when running tests, the test runner seeing a models
    # package tries to import it directly, failing to do so
    import sys

    if 'test' not in sys.argv:
        raise e

__all__ = [
    "EMAIL_TYPE",
    "Notification",
    "PENDING_STATE",
    "READ_STATE",
    "SENT_STATE",
    "WebNotification",
    "WEB_TYPE",
]
