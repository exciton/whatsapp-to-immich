#!/bin/sh
#
cd /working
rm encrypted_backup.key
rm msgstore.db
wacreatekey --hex ${WHATSAPP_ENCRYPTION_KEY} || exit
wadecrypt encrypted_backup.key /data/Databases/msgstore.db.crypt15 msgstore.db || exit
mkdir /working/albums
python /usr/src/app/do.py || exit
rm encrypted_backup.key
rm msgstore.db
immich-go upload from-folder  -s ${IMMICH_URL} -k ${IMMICH_API_KEY} /working/albums --tag WhatsApp --client-timeout 120m --folder-as-album FOLDER --no-ui || exit
rm /working/albums -r
mv /working/latest_extract_timestamp /working/latest_upload_timestamp
