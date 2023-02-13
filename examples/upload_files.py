from docflow import APIClient, APIClientFileExistsException
from bson import ObjectId
import glob


files_dir = "files/*"
email = "tester@docflow.ai"
password = "tester2022"
owner_id = ObjectId("62eb75e82962bd0fd0e626b5")

with APIClient(email=email, password=password, owner_id=owner_id) as api:
    print(api.is_logged_in())
    print(api.get_document_types())

    for filename in glob.glob(files_dir):
        try:
            api.upload_document(filename, doctype='incomingInvoice', split_pages=False, exception_if_exists=False)
        except APIClientFileExistsException as e:
            print(e.message)
