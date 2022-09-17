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
* `-p` (no <u>p</u>refix) - prevents prefixing a timestamped string to the uploaded file's name

#### As a Bash script:
*Requires having set the `python3` command to a version of Python >= 3.7.*

It's possible to use [the provided bash script](/backup-to-drive.sh), which can be installed using the following command:
```bash
sudo ln -s <full path to this repo locally>/backup-to-drive.sh /bin/backup-to-drive
```

After that, it can be used in the following manner (with same options as above):
```bash
backup-to-drive <filename>
```
