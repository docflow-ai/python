from docflow import APIClient, APIClientFileExistsException
from bson import ObjectId
from pprint import pprint

files_dir = "files/*"
email = "tester@docflow.ai"
password = "tester2022"
owner_id = ObjectId("62eb75e82962bd0fd0e626b5")

with APIClient(email=email, password=password, owner_id=owner_id) as api:
    doc = api.get_document_info(ObjectId("62eba7ba5ddf632cd132739f"))

    print("ID:", doc.id)
    print("Name:", doc.name)
    print("Doctype:", doc.doctype)
    print("Step:", doc.step)
    print("Created:", doc.createdAt)
    print("Updated:", doc.updatedAt)
    print("User ID:", doc.userId)
    print("Predicted:", doc.predicted)

    for page in doc.pages:
        pprint(page)

    for field in doc.fields:
        pprint(field)

    for key, cache in doc.cache.items():
        print(key, cache)


