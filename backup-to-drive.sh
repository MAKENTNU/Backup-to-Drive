#!/bin/bash
set -euo pipefail

no_prefix="false"

# Code based on https://stackoverflow.com/a/63421397
args=()
while [ $OPTIND -le "$#" ]; do
    if getopts i:p option; then
        case $option in
        i) folder_id="$OPTARG" ;;
        p) no_prefix="true" ;;
        \?) exit 1 ;;
        esac
    else
        args+=("${!OPTIND}")
        ((OPTIND++))
    fi
done

num_args=${#args[@]}

if [[ $num_args -ne 1 ]]; then
    echo "Usage: backup-to-drive <file> [-i <Google Drive folder ID>] [-p (no prefix)]"
    exit 1
fi

cd "$(dirname "$0")"
sudo python3 ./backup_to_drive.py "$@"
