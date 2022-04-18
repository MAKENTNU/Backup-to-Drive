import mimetypes
import sys
from datetime import datetime
from pathlib import Path
from sys import argv, exit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import settings
from util.logging_utils import logger


if len(argv) != 2:
    python_command = Path(sys.executable).name if sys.executable else "<Python command>"
    logger.error(f"Usage: {python_command} backup_to_drive.py <filename>")
    exit(1)

file_type_dot = argv[1].rfind(".")
original_name = argv[1]

backup_name = f'backup_{datetime.now().strftime("%Y-%m-%d_%Hh_%Mm")}.{original_name}'
mimetype, _encoding = mimetypes.guess_type(backup_name)

# Code based on https://developers.google.com/drive/api/quickstart/python#step_2_configure_the_sample
creds = None
if Path(settings.TOKEN_FILENAME).exists():
    creds = Credentials.from_authorized_user_file(settings.TOKEN_FILENAME, settings.GOOGLE_API_SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        logger.error("Must obtain new token. Please run 'obtain_new_token.py' manually.")
        exit(1)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

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
