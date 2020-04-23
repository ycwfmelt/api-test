import requests
import attr

from ..LibraryBase import Singleton


@attr.s
class AbstractHttpClient(metaclass=Singleton):
    _url = attr.ib(validator=attr.validators.instance_of(str))
    _options = attr.ib(default={'followRedirect': False,
                                'showContent': False,
                                'insecure': False,
                                'getAllMessage': False,
                                'verbose': False})

    def request(self, method, path, headers=None, options=None, payload=None):
        raise Exception('request not implement')

    def request(self, method, path, headers=None, options=None, payload=None):
        raise Exception('request not implement')

    def head(self, url, headers=None, options=None):
        raise Exception('head method not implement')

    def get(self, url, headers=None, options=None):
        raise Exception('get method not implement')

    def post(self, url, payload, headers=None, options=None):
        raise Exception('post method not implement')

    def put(self, url, payload, headers=None, options=None):
        raise Exception('put method not implement')

    def delete(self, url, headers=None, options=None, payload=None):
        raise Exception('delete method not implement')

    def options(self, url, payload, headers=None, options=None):
        return self.request('OPTIONS', url, headers, options, payload)

    def _formUrl(self, path):
        if self._isUrl(path):
            return path
        return self._url + path

    def _isUrl(self, path: str):
        if path.startswith("http://") or path.startswith("https://"):
            return True
        return False



class ConfigInitError(Exception):
    def __init__(self, message):
        self.message = message
