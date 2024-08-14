import json, os, re
import filetype
import base64
from io import BytesIO
from datetime import datetime
from requests import Session, Response
from hashlib import sha1, sha256
from bson import ObjectId
from PyPDF2 import PdfFileReader, PdfFileWriter
from docflow.exceptions import *
from docflow.document import Document


class APIClient:
    STEPS = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    base_url = 'https://api.docflow.ai'
    logged = False
    session = None
    doctypes = []
    current_owner_id = None
    owners = []

    def __init__(self, email: str = None, password: str = None, token: str = None, owner_id: ObjectId = None):
        self.session = Session()
        if email and password:
            self.login(email, password)
        elif token:
            self.login_with_token(token)
        else:
            APIClientException("Wrong authentication method", 500)
        if owner_id:
            self.change_owner(owner_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    @staticmethod
    def _process_error(response: Response):
        if response.status_code == 500:
            raise APIClientException("Fatal error", response.status_code)

        if response.status_code != 200:
            obj = response.json()
            raise APIClientException(obj.get('message'), response.status_code)

    def is_logged_in(self):
        return self.logged

    def login(self, email: str, password: str) -> bool:
        def parse_id(o: dict) -> dict:
            o['id'] = ObjectId(o['id'])
            return o

        if not re.match('^[a-f0-9]{64}$', password, re.IGNORECASE):
            password = sha256(password.encode('utf8')).hexdigest()

        response = self.session.post(f'{self.base_url}/user/login',
                                     data=json.dumps({'email': email, 'password': password}),
                                     headers={'Content-Type': 'application/json'})
        self._process_error(response)
        self.logged = True
        obj = response.json()
        self.owners = list(map(parse_id, obj['user'].get('owners', [])))
        return True

    def login_with_token(self, token) -> bool:
        def parse_id(o: dict) -> dict:
            o['id'] = ObjectId(o['id'])
            return o

        response = self.session.post(f'{self.base_url}/user/login-by-token',
                                     data=json.dumps({
                                         'type': 'api-client',
                                         'vendor': 'Docflow',
                                         'model': 'python',
                                         'version': '0.1.1'
                                     }),
                                     headers={'Content-Type': 'application/json', 'Token': str(token)})

        self._process_error(response)
        self.logged = True
        obj = response.json()
        self.owners = list(map(parse_id, obj['user'].get('owners', [])))
        return True

    def logout(self) -> bool:
        if self.session:
            self.session.close()
        return True

    def change_owner(self, owner_id: ObjectId) -> bool:
        owners_ids = list(map(lambda o: o['id'], self.owners))
        if owner_id not in owners_ids:
            raise APIClientException("Wrong owner ID")
        response = self.session.post(f'{self.base_url}/user/change-owner', data=json.dumps({"id": str(owner_id)}), headers={'Content-Type': 'application/json'})
        self._process_error(response)
        obj = response.json()
        self.current_owner_id = obj.get('currentOwnerId')
        return True

    def document_hash_exists(self, hash: str) -> bool:
        response = self.session.get(f'{self.base_url}/document/hash/{hash}', headers={'Content-Type': 'application/json'})
        self._process_error(response)
        obj = response.json()
        if obj.get('success') and obj.get('document') is not False:
            return True
        return False

    def get_owners(self):
        return zip(list(map(lambda o: o['id'], self.owners)), self.owners)

    def get_document_types(self) -> list:
        if not len(self.doctypes):
            response = self.session.get(f'{self.base_url}/doctypes', headers={'Content-Type': 'application/json'})
            self._process_error(response)
            self.doctypes = list(map(lambda o: o['id'], response.json()))

        return self.doctypes

    def get_document_info(self, doc_id: ObjectId) -> Document:
        response = self.session.get(f'{self.base_url}/document/info/{str(doc_id)}', headers={'Content-Type': 'application/json'})
        self._process_error(response)
        obj = response.json()
        if not obj.get('ownerId', False):
            raise APIClientException('Missing owner', 404)

        self.change_owner(ObjectId(obj.get('ownerId')))

        response = self.session.get(f'{self.base_url}/document/{str(doc_id)}', headers={'Content-Type': 'application/json'})
        self._process_error(response)
        obj = response.json()

        return Document.from_json(obj)

    def get_document_list(self, date_from: datetime, date_to: datetime, doctype: str = None, steps: list = STEPS) -> list:
        workflow = {}
        if doctype:
            workflow[doctype] = steps
        else:
            for doctype in self.get_document_types():
                workflow[doctype] = steps

        response = self.session.post(f'{self.base_url}/documents/ids', headers={'Content-Type': 'application/json'}, data=json.dumps({
            'project': '',
            'sortField': '_id',
            'sortOrder': -1,
            'filters': {
                'createdAtFrom': date_from.strftime(Document.DATE_FORMAT),
                'createdAtTo': date_to.strftime(Document.DATE_FORMAT),
                'workflow': workflow
            }
        }))
        self._process_error(response)
        obj = response.json()

        return list(map(lambda o: ObjectId(o), obj.get('data'))) if obj.get('total', 0) else []

    def upload_document(self, file_path: str, doctype: str, file_name: str = None, split_pages: bool = True, exception_if_exists: bool = False, owner_id: ObjectId = None) -> bool:
        if doctype not in self.get_document_types():
            raise APIClientException("Document type doesn't exists!")

        if not self.is_logged_in():
            raise APIClientException("You are not logged in!")

        if not self.current_owner_id:
            raise APIClientException("You must set owner!")

        if owner_id:
            self.change_owner(owner_id)

        file_name = os.path.basename(file_path) if not file_name else file_name
        if file_path.lower().endswith(".pdf"):
            pages = []
            pdf = PdfFileReader(file_path, strict=False)
            for page in range(pdf.getNumPages()):
                page_handler = BytesIO()
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                pdf_writer.write(page_handler)
                pages.append(page_handler.getvalue())
                #print('Created: {}'.format(output_filename))

            for doc in self._create_doc_object(file_name, pages, doctype=doctype, split=split_pages, exception_if_exists=exception_if_exists):
                #print(file_name, doc)

                response = self.session.post(f'{self.base_url}/document', data=json.dumps(doc), headers={'Content-Type': 'application/json'})
                self._process_error(response)
                obj = response.json()
                print(file_name, obj.get('id'))

        else:
            with open(file_path, "rb") as file:
                body = file.read()
                for doc in self._create_doc_object(file_name, [body], doctype=doctype, split=False, exception_if_exists=exception_if_exists):
                    #print(file_name, doc)

                    response = self.session.post(f'{self.base_url}/document', data=json.dumps(doc), headers={'Content-Type': 'application/json'})
                    self._process_error(response)
                    obj = response.json()
                    print(file_name, obj.get('id'))

        return True

    def add_payments(self, transactions: list) -> bool:
        response = self.session.post(f'{self.base_url}/payments', data=json.dumps(transactions), headers={'Content-Type': 'application/json'})
        self._process_error(response)
        return response.json()

    def _create_doc_object(self, name: str, pages: list, doctype: str, split=True, exception_if_exists=False) -> list:
        docs = [{"name": name, "origin": [], "documentType": doctype, "process": 0}]
        page = 0
        for i, body in enumerate(pages):
            last_doc = docs[-1]
            kind = filetype.guess(body)
            if not kind:
                raise APIClientDocumentException("Problem with document type")
            b64body = base64.b64encode(body).decode('ascii')
            b64data = f'data:{kind.mime};base64,{b64body}'
            hash = sha1(b64data.encode('utf8')).hexdigest()

            if exception_if_exists and self.document_hash_exists(hash):
                raise APIClientFileExistsException(f'Document {name} with hash {hash} exists!')

            last_doc["origin"].append({
                "name": name,
                "type": kind.mime,
                "data": b64data,
                "hash": hash,
                "page": page
            })

            if split and i < len(pages) - 1:
                docs.append({"name": name, "origin": []})
            else:
                page += 1

        return docs

