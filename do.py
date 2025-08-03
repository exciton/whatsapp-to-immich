import os
import shutil
import sqlite3
import csv
import re
from sanitize_filename import sanitize

def get_list_of_phones(string):
  phones = []
  for s in string.split(' ::: '):
    phones.append(re.sub(r'\D+', '', s))
  return phones 

phonebook = {}
def build_phonebook_from_csv(contact_csv):

  # try:
    with open(contact_csv, mode="r") as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for row in csv_reader:
        for i in range(1, 8):
          list_of_phones = get_list_of_phones(row[f'Phone {i} - Value'])
          for phone in list_of_phones:
            phonebook[phone[-10:]] =  ' '.join([row['First Name'], row['Last Name']])
  # except FileNotFoundError:
  #   print("No contacts.csv file found!")

def find_name_from_csv(phone):
  try:
    return phonebook[phone[-10:]]
  except KeyError:
    return None


build_phonebook_from_csv('/data/contacts.csv') #TODO: Handle  no contacts.csv
conn = sqlite3.connect('/working/msgstore.db')
path_to_whatsapp = "/data"
path_to_sorted_images = "/working/albums"
try:
  with open("/working/latest_upload_timestamp") as f:
    latest_upload_timestamp = f.read()
except FileNotFoundError:
  latest_upload_timestamp = "0"


cursor = conn.execute('''
select
  chat.subject,
  file_path,
  mime_type,
  message.timestamp,
  replace(jid.raw_string, "@s.whatsapp.net", "")
from `message_media` 
left join `chat` on message_media.chat_row_id = chat._id
left join `message` on message_media.message_row_id = message._id
left join `jid` on chat.jid_row_id = jid._id
where
  (`mime_type` like '%image%' or
  `mime_type` like '%video%') and
  file_path is not null and
  message.timestamp > {}                   
  ;
'''.format(latest_upload_timestamp))

    #chat.subject is not null and



for image in cursor:
  folder = image[0]
  if folder is None:
    folder = find_name_from_csv(image[4])
  if folder is None:
    print("Couldn't find name for {}".format(image[4])) 
  else: #TODO: Use phone number as a fallback maybe?

    path_to_chat_images = os.path.join(path_to_sorted_images, sanitize(folder))
    try:  
      if not os.path.exists(path_to_chat_images):
        os.mkdir(path_to_chat_images)
    except OSError as e:  
      print ("Creation of the directory {} failed \n {}".format(path_to_chat_images, e.strerror))
      pass

    try:
      path_to_file = os.path.join(path_to_whatsapp, image[1])
      is_file = os.path.isfile(path_to_file)
      path_to_new_file = os.path.join(path_to_chat_images, os.path.basename(image[1]))
      if is_file:
        try:
          shutil.copyfile(path_to_file, path_to_new_file)
          # print("{} copied in {}".format(image, person[1]))
        except:  
          print ("Copy failed for {} to {}".format(path_to_file, path_to_new_file))
    except:
      print("couldn't find file")

cursor = conn.execute('''select max(message.timestamp) from `message`;''')
with open("/working/latest_extract_timestamp", "w") as f:
  f.write("{}".format(cursor.fetchone()[0]))

conn.close()
