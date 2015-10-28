__author__ = 'jarfy'
from ReadFile import *
from hashmap import *

test = ReadFile()
data = test.readFile("data.txt")
formate = test.getType()
operator = MovieIndex(formate)
operator.MovieHash(data)
print "show movie index"
print operator.hashTable
print
print "put 46th record into index"
operator.Put(46, "The Abyss,1970,LaserDisc,Science Fiction,James Cameron,James Cameron,USA,20th Century Fox,$0.00")
print operator.hashTable
print
print "Find all movies made in 2000"
operator.Get("2000")
print
print "Find all movies made in 2005"
operator.Get("2005")
print
print "Find all movies made in 2010"
operator.Get("2010")
print
print "Find all DVD movies made in 1977"
operator.Get("1977|DVD")
print
print "Find all VHS movies made in 1990"
operator.Get("1990|VHS")
print
print "Find all DVD movies made in 2001"
operator.Get("2001|DVD")
print
print "Remove 38th record from movie index"
operator.Remove("38")
print operator.hashTable