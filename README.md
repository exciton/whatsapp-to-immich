WhatsApp to Immich Uploader

What it does:

- Decrypt your WhatsApp message database
- Reads in database (starting at timestamp from last run) and contacts list
- Copies media into folders (one per group chat or contact)
- Uploads folders as albums into Immich using immich-go
- Saves timestamp of last message as starting point for next run
- Deletes copied media

How to use it:

- Set up WhatsApp to use E2E encryption to backup your messages
- Copy the whole backup folder to your server
- Download your contacts in Google CSV format
- Run this docker image with the following environment variables
  -- BACKUP_LOCATION - directory on server containing the backup data
  -- WORKING_LOCATION - directory on server to store images temporarily, keep index timestamp, and contacts.csv
  -- WHATSAPP_ENCRYPTION_KEY - key you exported from WhatsApp
  -- IMMICH_API_KEY - API key to enable immich upload
  -- IMMICH_URL - URL of immich server

Features that could be added in future:

- Handle individual chats which aren't in contact list better (maybe fallback to phone number?). Currently they are skipped.
- Select which chats/individuals to include or exclude in the upload (maybe use WhatsApp lists for this?)
- Select whether to include/exclude media sent from self
- Add other metadata from WhatsApp database to uploaded media (e.g. Name of person who sent the photo, exact timestamp, caption)
- Rewrite as a phone app to avoid double-handling and use Contacts API to get names (instead of contacts csv)
