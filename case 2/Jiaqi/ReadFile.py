__author__ = 'jarfy'

class ReadFile:
    def __init__(self):
        # self.type = {}
        self.type = []
        self.record = []

    def readFile(self, filename):
        fhand = open(filename)
        for line in fhand:
            word = line.split(',')
            self.record.append(word[:-1])
            # print self.record
            if word[2] not in self.type:
                self.type.append(word[2])
        # print self.type
        return self.record


    def getType(self):
        return self.type