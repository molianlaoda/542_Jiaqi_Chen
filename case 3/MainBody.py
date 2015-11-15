import os
import sys
import cPickle
from UserDict import DictMixin

# Try using cPickle and cStringIO if available.
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


__all__ = ['fakeopen', 'FakeDict']
__author__ = 'Chan'


class FakeDict(DictMixin):
    """
    A dictionary-like object.
    It will synchronize with file on disk every time it closes.
    With writeback = True, instruction like dict[key].append(data) will be record. Otherwise it will not.
    Highly recommended to synchronize every times fetching or modifying data.
    The value of the 'dict' should be able to dump by simplejson.
    """
    def __init__(self, filename):
        # Cache trace the modification of mutable entries.
        self.key = ''
        self.filename = filename
        try:
            self.dbfile = open(filename, 'r')
            self.alldata = cPickle.load(self.dbfile)
            self.dbfile.close()
        except (IOError, ValueError) as e:
            print e
            self.alldata = {'metadata': {}}

    def __getitem__(self, key):
        try:
            return self.alldata[key]
        except KeyError:
            print 'No key named: ' + key

    def __setitem__(self, key, value):
        self.key = key
        assert sys.getsizeof(value) <= 1048576, 'The size of the bytearray must be smaller or equal to 1MB!'
        self.alldata[key] = value
        self.alldata['metadata'][key] = sys.getsizeof(value)

    def __len__(self):
        return len(self.alldata)

    def __delitem__(self, key):
        try:
            del self.alldata[key]
            del self.alldata['metadata'][key]
        except KeyError:
            pass

    def getMeta(self, key):
        return self.alldata['metadata'][key]

    def keys(self):
        return self.alldata.keys()

    def sync(self):
        self.dbfile = open(self.filename, 'w')
        cPickle.dump(self.alldata, self.dbfile, protocol=1)
        if os.path.getsize(self.filename) > 4*1024*1024:
            print 'File size exceeds the line!'
            print 'Rolling back...'
            del self[self.key]
        self.dbfile.close()

    def clearall(self):
        key_list = self.keys()
        for key in key_list:
            if key != 'metadata':
                del self[key]

    def close(self):
        # Synchronize with .db file on disk when closing.
        try:
            self.sync()
        finally:
            self.alldata = None


def fakeopen(filename):
    return FakeDict(filename)
