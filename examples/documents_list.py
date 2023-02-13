from docflow import APIClient, APIClientFileExistsException
from bson import ObjectId
from pprint import pprint
from datetime import datetime, timedelta

files_dir = "files/*"
email = "tester@docflow.ai"
password = "tester2022"
owner_id = ObjectId("62eb75e82962bd0fd0e626b5")

with APIClient(email=email, password=password, owner_id=owner_id) as api:
    print(api.get_document_types())

    date_to = datetime.utcnow()
    date_from = date_to - timedelta(days=7)

    for doc_id in api.get_document_list(date_from=date_from, date_to=date_to):
        doc = api.get_document_info(doc_id)
        print(doc)

    for doc_id in api.get_document_list(date_from=date_from, date_to=date_to, doctype='incomingInvoice'):
        doc = api.get_document_info(doc_id)
        print(doc)