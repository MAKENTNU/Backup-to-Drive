import logging


GOOGLE_API_SCOPES = ['https://www.googleapis.com/auth/drive.file']

CREDENTIALS_FILENAME = 'credentials.json'

BACKUP_TEAM_DRIVE_FOLDER_ID = 'xxxxxxxxxxxxxxxxxxx'

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': "{message}",
            'style': '{',
        },
        'verbose': {
            'format': "{levelname}\t| {name}\t|\t{message}",
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': logging.DEBUG,
        },
    },
    'loggers': {
        'util': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# Set local settings
try:
    from local_settings import *
except ImportError:
    pass
