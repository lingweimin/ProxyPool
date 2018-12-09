from datetime import datetime
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from proxypool.config import DATABASE_URI, DATABASE_NAME


def create_db():
    client = MongoClient(DATABASE_URI)
    return client[DATABASE_NAME]

db = create_db()


class TableBase:
    _tablename = None

    def add(self, obj):
        if isinstance(obj, self.__class__):
            inserted_id = self._query.insert_one(obj.to_json()).inserted_id
            return inserted_id

    def get_one(self, value, by='_id'):
        return self._query.find_one({by: value})

    def count(self):
        return self._query.count()

    def to_json(self):
        return self.__dict__


class Proxy(TableBase):
    _tablename = 'proxy'
    _query = db[_tablename]

    def __init__(self, **kwargs):
        if 'updated_date' not in kwargs.keys():
            kwargs.update({'updated_date': datetime.now()})
        self.__dict__ = kwargs

    def pop(self):
        if self.count() > 0:
            oldest = self._query.find().sort('updated_date', ASCENDING).limit(1)[0]
            self._query.delete_one({'_id': oldest['_id']})
            return oldest

    def get(self, count):
        if self.count() >= count:
            proxies = self._query.find().sort('updated_date', ASCENDING).limit(count)
            return proxies[0] if count == 1 else proxies
        else:
            raise ValueError('Not enough records.')

    def update(self, _id):
        self._query.update_one({'_id': _id}, {"$set": {'updated_date': datetime.now()}})

db.Proxy = Proxy()




