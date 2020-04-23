import requests

from .httpClient import AbstractHttpClient


class SessionHttpClient(AbstractHttpClient):

    def __init__(self, url, options=None):
        super(SessionHttpClient, self).__init__(url, options)
        self._session = requests.Session()
        self.proxies()

    def request(self, method, path, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        kwargs.setdefault('verify', True)

        request_url = self._formUrl(path)

        response = self._session.request(method, request_url, **kwargs)
        response.raise_for_status()

        return response

    def get(self, path, params=None):
        return self.request('GET', path, params=params)

    def post(self, path, **kwargs):
        """接受 `data`, `json`, `files`
        """
        return self.request('POST', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('DELETE', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('PUT', path, **kwargs)

    def proxies(self):
        from ..Configure import Conf
        self._session.proxies = Conf.getInstance('http_proxies').all
