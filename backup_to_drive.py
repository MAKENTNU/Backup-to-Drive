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


if len(argv) != 2:
    python_command = Path(sys.executable).name if sys.executable else "<Python command>"
    logger.error(f"Usage: {python_command} backup_to_drive.py <filename>")
    exit(1)

original_name = argv[1]

backup_name = f'backup_{datetime.now().strftime("%Y-%m-%d_%Hh_%Mm")}.{original_name}'
mimetype, _encoding = mimetypes.guess_type(backup_name)

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

logger.info(f"Uploading '{original_name}' to Drive with the filename '{backup_name}'")
# Code based on https://developers.google.com/drive/api/guides/folder#create_a_file_in_a_folder
media = MediaFileUpload(original_name, mimetype=mimetype)
service.files().create(
    supportsTeamDrives=True,
    media_body=media,
    body={
        "parents": [settings.BACKUP_TEAM_DRIVE_FOLDER_ID],
        "name": backup_name,
    }
).execute()
logger.info("Backup finished.")
