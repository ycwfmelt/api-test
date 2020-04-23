from ..LibraryBase import cproperty


class Conf:
    """接收初始化参数"""
    _sub = {}

    def __new__(cls, initConf=None):
        cls._config = {}
        if (initConf):
            if (isinstance(initConf, str)):
                cls._handleFile(initConf)
            elif(isinstance(initConf, dict)):
                cls._config.update(initConf)
            else:
                print(type(initConf))
        return cls

    @staticmethod
    def getInstance(name):
        return Conf._sub[name]

    @staticmethod
    def setInstance(name, cls):
        Conf._sub[name] = cls

    @cproperty
    def all(cls):
        return cls._config

    @cproperty
    def testbed(cls):
        return Conf._sub['testbed'].all

    @cproperty
    def testbed_url(cls):
        return cls.testbed['urls']

    @cproperty
    def testbed_db(cls):
        return cls.testbed['db']

    @classmethod
    def _handleFile(cls, initConf):
        from simple_test.tools import YamlConfigLoader

        conf = YamlConfigLoader(initConf)
        cls._config.update(conf)

    @staticmethod
    def createCls(name):
        return type(name, (Conf,), {})
