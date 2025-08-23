# Backup-to-Drive

## 🛠️ Setup

1. Start by
   [creating a service account for your Google Cloud project](https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount).

1. Create a `.env` file in the same folder as this README, and paste in the following
   contents:
   ```dotenv
   DRIVE_BACKUP_FOLDER_ID='<folder ID>'
   ```
   where `<folder ID>` is replaced with the ID of the Google Drive folder you want to
   upload to.
   (Alternatively, this ID can be provided using the `-i` option described below.)

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

1. Install dev dependencies:
   ```bash
   uv sync --group dev
   ```


## 🚀 Usage

Run the following command to upload `<filename>` to the previously specified folder:
```bash
uv run backup_to_drive.py <filename>
```

If using a Unix-based operating system (like Linux or macOS), the command can also be
run like:
```bash
./backup_to_drive.py <filename>
```

### Options:

* `-i, --folder-id <Google Drive folder ID>` - defaults to `DRIVE_BACKUP_FOLDER_ID`
* `-p, --no-prefix` - prevents prefixing a timestamped string to the uploaded file's
  name


## 🧹 Linting

Run:
```bash
pre-commit run --all-files
```
