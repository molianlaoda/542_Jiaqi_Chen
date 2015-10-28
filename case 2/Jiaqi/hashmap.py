__author__ = 'jarfy'
from ReadFile import *

class MovieIndex:
    def __init__(self, type):
        self.hashTable = [["-1" for x in range(10)] for y in range(10)]
        # self.record = record
        self.type = type

    def MovieHash(self, data, key = 'all'):
        #compute the hash number
        for each in data:
            bucket = int(each[1]) % 10
            if key == 'all':
                content = str(each[1]) + '0' + str(self.type.index(each[2])) +\
                          '0' + str(data.index(each))
            else:
                content = str(each[1]) + '0' + str(self.type.index(each[2])) +\
                          '0' + str(key)
            for block in range(0,9):
                if self.hashTable[bucket][block] == content:
                    break
                elif self.hashTable[bucket][block] == '-1':
                    self.hashTable[bucket][block] = content
                    break

    def Put(self, key, data):
        container = []
        word = data.split(',')
        container.append(word[:-1])
        if word[2] not in self.type:
            self.type.append(word[2])
        self.MovieHash(container, key)

    def Get(self, query):
        locate_file = ReadFile()
        record = locate_file.readFile("data.txt")
        if '|' in query:
            info = query.split('|')
            year_index = int(info[0]) % 10
            movie_type = self.type.index(info[1])
            index = str(info[0]) + '0' + str(movie_type)
            for each in self.hashTable[year_index]:
                if each[:6] == index:
                    location = int(each[6:])
                    print ", ".join(record[location])
                elif each == '-1':
                    return "The record is not in the database"
        else:
            year_index = int(query) % 10
            for each in self.hashTable[year_index]:
                if each == '-1':
                    # print "no more record in query"
                    break
                else:
                    if each[:4] == query:
                        location = int(each[6:])
                        print ", ".join(record[location])

    def Remove(self, key):
        locate_file = ReadFile()
        record = locate_file.readFile("data.txt")
        for year in self.hashTable:
            for each in year:
                if each[-2:] == key:
                    year.remove(each)
                    year.append('-1')

