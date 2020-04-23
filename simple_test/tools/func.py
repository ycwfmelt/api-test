from collections import namedtuple
from functools import partial, wraps

import pytest

from simple_test.core import Mapper
from simple_test.core import Conf


# ------- begin decorator -------

def data_for_return(field: list = None) -> tuple:
    """指定要返回的请求中的数据\n
    Example:
    >>> @data_for_return(['code', 'status'])
    >>> def isLogin():
    >>>     return
    """
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            ret_of_req = func(*args, **kwargs)
            ret_of_req.raise_for_status()
            data = ret_of_req.json()['data']

            if field:
                _data = namedtuple(func.__name__, field)
                _data = _data(*[data.get(key)for key in field])
            else:
                _data = data

            return _data
        return wrapper
    return decorated


class apiRequests:
    """`apiRequests` 装饰器
    """

    def __init__(self, method, func):
        self.__name__ = func.__name__
        self._method = method
        self._func = _func_belong(func)

    def __call__(self, *args, **kwargs):
        client = Mapper.value(self._func[0])
        request_path = self._func_request_path(self._func)
        if self._method == 'GET':
            return self.get(client, request_path, *args, **kwargs)
        else:
            if args:
                kwargs.update(data=args[0])
            return self.post(client, request_path, **kwargs)

    def get(self, client, request_path, *args, **kwargs):
        return client.get(request_path, *args, **kwargs)

    def post(self, client, request_path, **kwargs):
        return client.post(request_path, **kwargs)

    @staticmethod
    def _func_request_path(func_meta) -> str:
        """根据 `module`,`class`,`function` 查找 Api Path
        """
        apipath = Conf.getInstance('apipath').all
        for item in func_meta:
            apipath = apipath.get(item)

        return apipath


class apiRequest:
    """用于装饰请求函数\n
    Example:
    >>> @apiRequest.get()
    >>> def isLogin(params):
    >>>     return
    """
    @staticmethod
    def get():
        return partial(apiRequests, 'GET')

    @staticmethod
    def post():
        return partial(apiRequests, 'POST')

# ------- end decorator -------


def _func_belong(func) -> list:
    """传入一个 `function`，返回他的 `module`,`class`,`function`
    """
    tree = func.__module__.split('.')[-1:]
    tree.extend(str(func).split()[1].split('.'))

    return tree
