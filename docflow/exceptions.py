
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


class APIClientFileExistsException(APIClientException):
    pass


class APIClientDocumentException(APIClientException):
    pass