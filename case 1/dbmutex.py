from multiprocessing import Process, Lock
import MainBody


_author__ = 'Chan'


class Client(object):
    def __init__(self, filename):
        self.filename = filename
        self.db = MainBody.open(self.filename)
        self.lock = Lock()

    def Put(self, key, data):
        key = str(key)
        data = str(data)
        # Meta data
        self.db[key] = data
        self.db.sync()

    def Get(self, key):
        key = str(key)
        try:
            # Meta data
            return self.db[key]
        finally:
            self.db.sync()

    def Remove(self, key):
        key = str(key)
        del self.db[key]
        self.db.sync()