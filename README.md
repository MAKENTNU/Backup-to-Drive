# Backup-to-Drive

### Usage:
Start by [creating a service account for your Google Cloud project](https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount).

Create a `local_settings.py` file and create a `DRIVE_BACKUP_FOLDER_ID` variable
with the ID of the Google Drive folder you want to upload to as value.

Run the following command to upload `<filename>` to the previously specified folder:
```bash
python backup_to_drive.py <filename>
```

#### Options:
* `-i <Google Drive folder ID>` - defaults to `DRIVE_BACKUP_FOLDER_ID`
