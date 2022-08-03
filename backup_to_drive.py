import mimetypes
import sys
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from sys import argv, exit

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import settings
from util.logging_utils import logger


# --- Parse command line arguments ---
if len(argv) != 2:
    python_command = Path(sys.executable).name if sys.executable else "<Python command>"
    logger.error(f"Usage: {python_command} backup_to_drive.py <filename>")
    exit(1)

original_name = argv[1]

# --- Initialize some variables ---
backup_name = f'backup_{datetime.now().strftime("%Y-%m-%d_%Hh_%Mm")}.{original_name}'
mimetype, _encoding = mimetypes.guess_type(backup_name)

# --- Create credentials ---
# Code based on https://developers.google.com/identity/protocols/oauth2/service-account#authorizingrequests
creds = None
try:
    creds = service_account.Credentials.from_service_account_file(settings.CREDENTIALS_FILENAME, scopes=settings.GOOGLE_API_SCOPES)
except (FileNotFoundError, JSONDecodeError, ValueError) as e:
    logger.exception(f"Error while parsing credentials from '{settings.CREDENTIALS_FILENAME}'.", exc_info=e)
    logger.error("Please use the following guide on creating service account credentials/keys:"
                 " https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount")
    exit(1)

service = build('drive', 'v3', credentials=creds)

# --- Upload the file ---
logger.info(f"Uploading '{original_name}' to Drive with the filename '{backup_name}'")
# Code based on https://developers.google.com/drive/api/guides/folder#create_a_file_in_a_folder
media = MediaFileUpload(original_name, mimetype=mimetype)
service.files().create(
    body={
        'parents': [settings.DRIVE_BACKUP_FOLDER_ID],
        'name': backup_name,
    },
    media_body=media,
    supportsAllDrives=True,
).execute()
logger.info("Backup finished.")
