from multiprocessing import Process, Lock
import MainBody
import sys


_author__ = 'Chan'


class Operate_src(object):
    def __init__(self, filename):
        self.filename = filename
        self.getdb = MainBody.fakeopen(self.filename)

    def Put(self, key, data):
        self.db = MainBody.fakeopen(self.filename)
        key = str(key)
        self.db[key] = data
        if key in self.db.keys():
            # print str(key) + " in db"
            print "show db keys after PUT " + key + " " +str(self.db.keys())
        else:
            print str(key) + " not in db"
            return
        self.db.sync()

    def Get(self, key):
        self.db = MainBody.fakeopen(self.filename)
        key = str(key)
        try:
            # Meta data
            return self.db[key]
        finally:
            self.db.sync()

    def Remove(self, key):
        self.db = MainBody.fakeopen(self.filename)
        key = str(key)
        try:
            print self.db.keys()
            if key not in self.db.keys():
                raise LookupError
            del self.db[key]
        except LookupError:
            print "Error: there is no %s exist" %key
        self.db.sync()

