import logging
import os
from typing import Final

from dotenv import load_dotenv

_envvars_loaded = load_dotenv()
if not _envvars_loaded:
    raise RuntimeError("Couldn't load any environment variables from `.env`")


GOOGLE_API_SCOPES: Final = ["https://www.googleapis.com/auth/drive.file"]

CREDENTIALS_FILENAME: Final = "credentials.json"

DRIVE_BACKUP_FOLDER_ID: Final = os.environ.get("DRIVE_BACKUP_FOLDER_ID")

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
