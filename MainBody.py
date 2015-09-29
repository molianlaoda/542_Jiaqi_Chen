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
        self.filename = filename
        try:
            self.dbfile = open(filename, 'r')
            self.alldata = cPickle.load(self.dbfile)
            # print str(sys.getsizeof(cPickle.dumps(self.alldata)))+'!'
            self.dbfile.close()
        except (IOError, ValueError) as e:
            print e
            self.alldata = {'metadata': {}}

    def __getitem__(self, key):
        try:
            return bytearray(self.alldata[key])
        except KeyError:
            print 'No key named: ' + key

    def __setitem__(self, key, value):
        assert sys.getsizeof(value) <= 1048576, 'The size of the bytearray must be smaller or equal to 1MB!'
        dumps_value = cPickle.dumps(value)
        self.alldata[key] = dumps_value
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
        self.dbfile.close()

    def close(self):
        # Synchronize with .db file on disk when closing.
        try:
            self.sync()
        finally:
            self.alldata = None


def fakeopen(filename):
    return FakeDict(filename)

test = fakeopen('/Users/Chan/Desktop/Test01.db')
test['A'] = bytearray(1048000)
print sys.getsizeof(cPickle.dumps(bytearray(1048000)))
test['B'] = bytearray(1048000)
test['C'] = bytearray(1048000)
test['D'] = bytearray(1048000)
test['E'] = bytearray(1048000)
test.close()

print os.path.getsize('/Users/Chan/Desktop/Test01.db')

test = fakeopen('/Users/Chan/Desktop/Test01.db')
print len(test['A'])
test.close()

test = fakeopen('/Users/Chan/Desktop/Test01.db')
print len(test['A'])
test.close()
