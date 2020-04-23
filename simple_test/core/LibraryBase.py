class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class cproperty(property):
    def __get__(self, obj, objtype=None):
        return super(cproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(cproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(cproperty, self).__delete__(type(obj))


class Mapper:
    _mapper_relation = {}

    @staticmethod
    def register(cls, value):
        Mapper._mapper_relation[cls] = value

    @staticmethod
    def exist(cls):
        if cls in Mapper._mapper_relation:
            return True
        return False

    @staticmethod
    def value(cls):
        return Mapper._mapper_relation[cls]
