import MainBody
import os

__author__ = 'Chan'


class Logging(object):
    path = 'data/log.db'

    def __init__(self):
        self.log = None

    def open(self):
        if os.path.isfile(self.path):
            self.log = MainBody.fakeopen(self.path)
        else:
            self.log = MainBody.fakeopen(self.path)
            self.log['records'] = []

    def record(self, table, key, idx1, idx2, old, new):
        self.log['records'].append([table, key, idx1, idx2, old, new])

    def recover(self, data):
        for record in self.log['records']:
            table, key, idx1, idx2, old, new = record[0], record[1], record[2], record[3], record[4], record[5]
            data[table][key][idx1][idx2] = new

        data.sync()

    def clearall(self):
        self.log.clearall()
        self.log.sync()

    def close(self):
        self.log.close()

    def sync(self):
        self.log.sync()