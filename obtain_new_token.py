import os.path
from json import JSONDecodeError
from sys import exit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import settings
from util.logging_utils import logger


# Code based on https://developers.google.com/drive/api/quickstart/python#step_2_configure_the_sample
creds = None
if os.path.exists(settings.TOKEN_FILENAME):
    creds = Credentials.from_authorized_user_file(settings.TOKEN_FILENAME, settings.GOOGLE_API_SCOPES)
if creds and creds.valid:
    continue_anyway = input("A valid token already exists. Obtain a new one anyway? (y/n) ")
    continue_anyway_lower = continue_anyway.lower()
    if continue_anyway_lower == "n":
        logger.info("Exiting.")
        exit(0)
    elif continue_anyway_lower != "y":
        logger.error(f"Unable to understand '{continue_anyway}'. Exiting.")
        exit(1)

if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
else:
    try:
        flow = InstalledAppFlow.from_client_secrets_file(settings.CREDENTIALS_FILENAME, settings.GOOGLE_API_SCOPES)
        creds = flow.run_console()
    except (FileNotFoundError, JSONDecodeError, ValueError) as e:
        logger.exception(f"Error while parsing credentials from '{settings.CREDENTIALS_FILENAME}'.", exc_info=e)
        logger.error("Please use the following guide on creating credentials:"
                     " https://developers.google.com/workspace/guides/create-credentials")
        exit(1)

# Save the credentials for the next run
with open(settings.TOKEN_FILENAME, 'w') as token:
    token.write(creds.to_json())

logger.info("Successfully obtained and wrote new token.")
