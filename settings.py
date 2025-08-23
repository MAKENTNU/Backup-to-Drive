import logging
from typing import Final


GOOGLE_API_SCOPES: Final = ["https://www.googleapis.com/auth/drive.file"]

CREDENTIALS_FILENAME: Final = "credentials.json"

DRIVE_BACKUP_FOLDER_ID: str

SOCKET_DEFAULT_TIMEOUT: Final = 5 * 60
NUM_UPLOAD_RETRIES: Final = 3

LOG_CONFIG: Final = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "{message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname}\t| {name}\t|\t{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": logging.DEBUG,
        },
    },
    "loggers": {
        "util": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
}

# Set local settings
try:
    from local_settings import *
except ImportError:
    pass
