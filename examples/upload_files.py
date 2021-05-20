from docflow import APIClient
from os import walk
import glob


files_dir = "files/*"
email = "branislav@vaculciak.sk"
password = "spustiwacco"
owner_id = "5e66088ea709987fd0669b07"
with APIClient(email=email, password=password, owner_id=owner_id) as api:
    print(api.is_logged_in())
    print(api.get_document_types())

    for filename in glob.glob(files_dir):
        api.upload_document(filename, type='incomingInvoice', split_pages=False)

        break

