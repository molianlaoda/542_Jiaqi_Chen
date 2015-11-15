import os
import sys
import simplejson as json
import bsddb
from UserDict import DictMixin

# Try using cPickle and cStringIO if available.
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


__all__ = ['open', 'FakeDict']
__author__ = 'Chan'


class FakeDict(DictMixin):
    """
    A dictionary-like object.
    It will synchronize with file on disk every time it closes.
    With writeback = True, instruction like dict[key].append(data) will be record. Otherwise it will not.
    Highly recommended to synchronize every times fetching or modifying data.
    The value of the 'dict' should be able to dump by simplejson.
    """
    def __init__(self, dict, writeback = True):
        # Cache trace the modification of mutable entries.
        self.dict = dict
        self.writeback = writeback
        self.cache = {}

    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            io = StringIO(self.dict[key])
            value = json.load(io)
            if self.writeback:
                self.cache[key] = value
        return bytearray(value)

    def __setitem__(self, key, value):
        assert sys.getsizeof(value) <= 1024, 'The size of the bytearray must be smaller or equal to 1MB!'
        if self.writeback:
            self.cache[key] = str(value)
        io = StringIO()
        json.dump(str(value), io)
        self.dict[key] = io.getvalue()

    def __len__(self):
        return len(self.dict)

    def __delitem__(self, key):
        try:
            del self.dict[key]
        except KeyError:
            pass

        try:
            del self.cache[key]
        except KeyError:
            pass

    def keys(self):
        return self.dict.keys()

    def sync(self):
        if self.writeback and len(self.cache):
            # If there are records in cache, synchronize them and put cache to empty.
            for key, value in self.cache.iteritems():
                self[key] = value
            self.cache = {}
        if hasattr(self.dict, 'sync'):
            self.dict.sync()
        else:
            print 'Cannot synchronized.'

    def close(self):
        # Synchronize with .db file on disk when closing.
        try:
            self.sync()
            try:
                self.dict.close()
            except AttributeError:
                pass
        finally:
            self.dict = None

def open(filename, openstyle = 'c', writeback = True):
    dbf = bsddb.hashopen(filename, flag = openstyle)
    return FakeDict(dbf, writeback)

test = open('Test.db')
test['A'] = bytearray(120)
print sys.getsizeof(bytearray(120))
test['B'] = bytearray(120)
test['C'] = bytearray(120)
test['D'] = bytearray(120)
test.close()

print os.path.getsize('Test.db')

