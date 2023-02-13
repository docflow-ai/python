from __future__ import annotations
from bson import ObjectId
from datetime import datetime
import pytz


class Document:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    TIMEZONE = "Europe/Bratislava"
    LOCAL_TIMEZONE = pytz.timezone(TIMEZONE)

    _id: ObjectId = None
    _userId: ObjectId = None
    _step: int = 0
    _doctype: str = None
    _name: str = None
    _predicted: bool = None
    _updatedAt: datetime = None
    _createdAt: datetime = None
    _pages: list = []
    _fields: list = []
    _cache: dict = []

    def __init__(self):
        pass

    def __str__(self):
        return f'#{self.id} : name({self.name}) doctype({self.doctype}) step({self.step}) createdAt({self.createdAt}) updatedAt({self.updatedAt})'

    @classmethod
    def from_json(cls, data: dict) -> Document:
        doc = Document()
        doc._id = ObjectId(data.get('id'))
        doc._name = str(data.get('name'))
        doc._doctype = str(data.get('doctype'))
        doc._userId = ObjectId(data.get('userId')) if data.get('userId', False) else None
        doc._createdAt = datetime.strptime(data.get('createdAt') + 'Z', cls.DATE_FORMAT)
        doc._updatedAt = datetime.strptime(data.get('updatedAt') + 'Z', cls.DATE_FORMAT)
        doc._step = int(data.get('step'))
        doc._predicted = bool(data.get('predicted'))

        for page in data.get('pages', []):
            page['fileId'] = ObjectId(page.get('_id'))
            del page['_id'], page['vision'], page['type']
            doc._pages.append(page)

        for field in data.get('fields', []):
            if field.get('bounds', {}).get('id', False):
                field['bounds']['id'] = ObjectId(field.get('bounds', {}).get('id'))
            if field.get('bboxes', None) is not None:
                del field['bboxes']
            if field.get('auto', None) is not None:
                del field['auto']
            doc._fields.append(field)

        doc._cache = data.get('cache', {})
        return doc

    @property
    def id(self) -> ObjectId:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def doctype(self) -> str:
        return self._doctype

    @property
    def step(self) -> int:
        return self._step

    @property
    def predicted(self) -> bool:
        return self._predicted

    @property
    def userId(self) -> ObjectId:
        return self._userId

    @property
    def createdAt(self) -> datetime:
        return self._createdAt

    @property
    def updatedAt(self) -> datetime:
        return self._updatedAt

    @property
    def pages(self) -> list:
        return self._pages

    @property
    def fields(self) -> list:
        return self._fields

    @property
    def cache(self) -> dict:
        return self._cache
