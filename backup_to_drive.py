#!/usr/bin/env -S uv run
import argparse
import mimetypes
import socket
from datetime import datetime
from json import JSONDecodeError
from sys import exit

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import settings
from util.logging_utils import logger


# --- Parse command line arguments ---
parser = argparse.ArgumentParser(description="Backup a file to a Google Drive folder.")
parser.add_argument("filename", type=str,
                    help="the (preferably absolute) filename of the file to be uploaded")
parser.add_argument("-i", "--folder-id", default=settings.DRIVE_BACKUP_FOLDER_ID, type=str,
                    help="the ID of the Google Drive folder that the file should be uploaded to")
parser.add_argument("-p", "--no-prefix", action='store_true',
                    help="won't prefix the uploaded file's name with a timestamped string")
args = parser.parse_args()

original_name = args.filename
drive_folder_id = args.folder_id
no_prefix = args.no_prefix

# --- Initialize some variables ---
if no_prefix:
    backup_name = original_name
else:
    now = datetime.now().replace(microsecond=0)
    backup_name = f"backup_{now.isoformat()}_{original_name}"
mimetype, _encoding = mimetypes.guess_type(backup_name)

socket.setdefaulttimeout(settings.SOCKET_DEFAULT_TIMEOUT)

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
logger.info(f"Uploading '{original_name}' to Drive (folder ID: '{drive_folder_id}') with the filename '{backup_name}'")
# Code based on https://developers.google.com/drive/api/guides/folder#create_a_file_in_a_folder
media = MediaFileUpload(original_name, mimetype=mimetype)
for i in range(settings.NUM_UPLOAD_RETRIES):
    try:
        uploaded_file = service.files().create(
            body={
                'parents': [drive_folder_id],
                'name': backup_name,
            },
            media_body=media,
            supportsAllDrives=True,
            fields='webViewLink',
        ).execute()
        logger.info(f"Backup finished! View the file at {uploaded_file.get('webViewLink')}")
        break
    except socket.timeout as e:
        # Let the exception crash the program if this is the last iteration
        if i == settings.NUM_UPLOAD_RETRIES - 1:
            raise e
