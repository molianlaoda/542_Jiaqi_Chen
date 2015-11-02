__author__ = 'jarfy'

class ReadFile(object):
    def __init__(self):
        # self.type = {}
        self.record = []
        self.content = []
        self.col = {'Name': 0, 'Year': 1, 'Format': 2, 'Genre': 3, 'Director': 4, 'Writer': 5, 'Country': 6, 'Maker': 7}

    def readFile(self, filename):
        try:
            fhand = open(filename)
        except IOError:
            print('Wrong Address')
        for line in fhand:
            word = line.split(',')
            self.content.append(word)

    def setattributes(self, *attr):
        attr_list = [self.col[att] for att in attr]
        for line in self.content:
            self.record.append(''.join(line[i] for i in attr_list))

'''
test = ReadFile()
test.readFile('data.txt')
'''