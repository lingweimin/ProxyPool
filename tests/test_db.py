import unittest
import random
from proxypool.db import db, Proxy


class DBProxyCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        ip = '.'.join([str(random.randint(0, 255)) for i in range(4)])
        proxy = Proxy(ip=ip, port='80')
        self.assertIsNotNone(db.Proxy.add(proxy))

    def _test_pop(self):
        proxy = db.Proxy.pop()
        print(proxy)
        self.assertIsNotNone(proxy)

    def test_get(self):
        proxies = db.Proxy.get(2)
        for proxy in proxies:
            print(proxy)
        self.assertTrue(5, proxies.count())

    def test_update(self):
        proxy = db.Proxy.get(1)
        d1 = proxy['updated_date']
        _id = proxy['_id']
        db.Proxy.update(_id)
        d2 = db.Proxy.get_one(_id, by='_id')['updated_date']
        self.assertNotEqual(d1, d2)
