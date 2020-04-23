import attr


@attr.s
class RobotFactory:
    _url = attr.ib(repr=True)
    _auth_uri = attr.ib()
    _auth_data = attr.ib(type=dict, repr=True)

    def _init_client(self):
        from .sessionClient import SessionHttpClient
        self._client = SessionHttpClient(url=self._url)
        
        return self

    def _sign_client(self):
        self._client.post(path=self._auth_uri,
                          data=self._auth_data, allow_redirects=True)
        return self

    def _get_client(self):
        return self._client

    @staticmethod
    def getConfigure(name: str, method='sso') -> dict:
        from .. import Conf
        if method == 'sso':
            url_configure = Conf.testbed_url.get(name, None)
            sso_configure = Conf.testbed_url.get('sso')
            return {
                'url': url_configure['uri'],
                'auth_uri': sso_configure['uri']+sso_configure['login'],
                'auth_data': url_configure['login'],
            }
        elif method == 'self':
            url_configure = Conf.testbed_url.get(name, None)
            return {
                'url': url_configure['uri'],
                'auth_uri': url_configure['login']['uri'],
                'auth_data': {key: url_configure['login'][key] for key in url_configure['login'].keys() - {'uri'}},
            }

    @staticmethod
    def getInstance(configure: dict):

        return RobotFactory(*list(configure.values())) \
            ._init_client() \
            ._sign_client() \
            ._get_client()
