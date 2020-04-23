import logging
import attr

import mysql.connector
from mysql.connector import errorcode

from ..LibraryBase import Singleton


@attr.s(hash=True)
class DBClient(metaclass=Singleton):
    _host = attr.ib(repr=True, hash=True)
    _port = attr.ib(converter=int, repr=True, hash=True)
    _user = attr.ib()
    _password = attr.ib()
    _db_name = attr.ib(repr=True, hash=True)
    _charset = attr.ib(default='utf8mb4')
    _conn = attr.ib(default=None)

    def __del__(self):
        if not isinstance(self._conn, type(None)):
            self._conn.close()

    def _connect_db(self):
        try:
            self._conn = mysql.connector.connect(
                host=self._host, port=self._port,
                user=self._user, password=self._password,
                database=self._db_name, charset=self._charset)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error(
                    f'数据库({self._name})建立连接时发生错误: 用户名或密码错误\n使用配置:{self}\n用户名:{self._user}\t密码:{self._password}')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error(
                    f'数据库({self._name})建立连接时发生错误: 数据库不存在\n使用配置:{self}')
            else:
                logging.error(
                    f"数据库({self._name})建立连接时发生错误: {err}\n使用配置:{self}")
            raise
        else:
            return self._conn

    @staticmethod
    def getConfigure(name: str) -> dict:
        from .. import Conf
        return Conf.testbed_db.get(name, None)

    @staticmethod
    def getInstance(configure: dict):

        return DBClient(*list(configure.values())) \
            ._connect_db() \
            .cursor()
