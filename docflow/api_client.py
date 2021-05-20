import json, os
import filetype
import base64
from requests import Session, Response
from hashlib import sha256
from PyPDF2 import PdfFileReader, PdfFileWriter


class APIClient:
    base_url = 'https://api.docflow.ai'
    logged = False
    session = None
    credentials = {'email': None, 'password': None}
    doctypes = []
    current_owner_id = None
    owners = []

    def __init__(self, email: str, password: str, owner_id: str = ""):
        self.session = Session()
        self.credentials = {'email': email, 'password': sha256(password.encode('utf8')).hexdigest()}
        self.login(self.credentials)
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

    def login(self, credentials) -> bool:
        response = self.session.post(f'{self.base_url}/user/login', data=json.dumps(credentials), headers={'Content-Type': 'application/json'})
        self._process_error(response)
        self.logged = True
        obj = response.json()
        self.owners = obj['user'].get('owners', [])
        return True

    def logout(self) -> bool:
        if self.session:
            self.session.close()
        return True

    def change_owner(self, owner_id: str) -> bool:
        owners_ids = list(map(lambda o: o['id'], self.owners))
        if owner_id not in owners_ids:
            raise APIClientException("Wrong owner ID")
        response = self.session.post(f'{self.base_url}/user/change-owner', data=json.dumps({"id": owner_id}), headers={'Content-Type': 'application/json'})
        self._process_error(response)
        obj = response.json()
        self.current_owner_id = obj.get('currentOwnerId')
        return True

    def get_owners(self):
        return zip(list(map(lambda o: o['id'], self.owners)), self.owners)

    def get_document_types(self) -> list:
        if not len(self.doctypes):
            response = self.session.get(f'{self.base_url}/doctypes', headers={'Content-Type': 'application/json'})
            self._process_error(response)
            self.doctypes = list(map(lambda o: o['id'], response.json()))

        return self.doctypes

    def upload_document(self, file_path: str, type: str, split_pages: bool = True, owner_id: str = "") -> bool:
        if type not in self.get_document_types():
            raise APIClientException("Document type doesn't exists!")

        if not self.is_logged_in():
            raise APIClientException("You are not logged in!")

        if not self.current_owner_id:
            raise APIClientException("You must set owner!")

        if owner_id:
            self.change_owner(owner_id)

        print(file_path, type, split_pages, self.current_owner_id)

        file_name = os.path.basename(file_path)

        if file_path.lower().endswith(".pdf"):
            print("PDF")
        else:
            print("image")
            with open(file_path, "rb") as file:
                body = file.read()
                kind = filetype.guess(body)
                b64body = base64.b64encode(body).decode('ascii')

                data = {
                    "name": file_name,
                    "origin": [{
                        "name": file_name,
                        "type": kind.mime,
                        "data": f'data:{kind.mime};base64,{b64body}',
                        "page": 0
                    }]
                }

                response = self.session.post(f'{self.base_url}/document', data=json.dumps(data), headers={'Content-Type': 'application/json'})
                self._process_error(response)
                obj = response.json()
                print(file_name, kind.mime, obj.get('_id'))

        return True

    #{"name":"IMG_6251.JPG","origin":[{"name":"IMG_6251.JPG","type":"image/jpeg","page":0,"data":"data:image/jpeg;base64,/9j/4AAQSkZJRg


class APIClientException(Exception):
    _code = 0
    _message = None

    def __init__(self, message: str, code: int = 500):
        self._message = message
        self._code = code

    def __str__(self):
        return str(f'{self._code}: {self._message}')

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message


class APIClientLoginException(APIClientException):
    pass

