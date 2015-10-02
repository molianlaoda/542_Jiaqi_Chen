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
<<<<<<< Updated upstream
    With writeback = True, instruction like dict[key].append(data) will be record. Otherwise it will not.
    Highly recommended to synchronize every times fetching or modifying data.
    The value of the 'dict' should be able to dump by simplejson.
=======
    Highly recommended to synchronize every times fetching or modifying data.
    The value of the 'dict' should be able to dump by cPickle.
>>>>>>> Stashed changes
    """
    def __init__(self, filename):
        # Cache trace the modification of mutable entries.
        self.key = ''
        self.filename = filename
        try:
            self.dbfile = open(filename, 'r')
            self.alldata = cPickle.load(self.dbfile)
<<<<<<< Updated upstream
            # print str(sys.getsizeof(cPickle.dumps(self.alldata)))+'!'
=======
>>>>>>> Stashed changes
            self.dbfile.close()
        except (IOError, ValueError) as e:
            print e
            self.alldata = {'metadata': {}}

    def __getitem__(self, key):
        try:
<<<<<<< Updated upstream
=======
            print "successfully get item " + str(key)
>>>>>>> Stashed changes
            return bytearray(self.alldata[key])
        except KeyError:
            print 'No key named: ' + key

    def __setitem__(self, key, value):
        self.key = key
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
        if os.path.getsize(self.filename) > 4*1024*1024:
            print 'File size exceeds the line!'
<<<<<<< Updated upstream
=======
            print 'Rolling back...'
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream

test = fakeopen('/Users/Chan/Desktop/Test01.db')
test['A'] = bytearray(1048000)
test.sync()
test['B'] = bytearray(1048000)
test.sync()
test['C'] = bytearray(1048000)
test.sync()
test['D'] = bytearray(1048000)
test.sync()
del test['B']
test['E'] = bytearray(1048000/2)
test['F'] = bytearray(1048000)
test.sync()
del test['C']
test['G'] = bytearray(1048000)
test.sync()
del test['E']
test['H'] = bytearray(1048000)
test.sync()
test.clearall()
test.close()

print os.path.getsize('/Users/Chan/Desktop/Test01.db')

=======
>>>>>>> Stashed changes
