 __author__ = 'jarfy'
import ReadFile
from HashTable import *


#  Test Case One
print('Test Case One --- Set Year and Format as Index.')
test = ReadFile.ReadFile()
test.readFile("data.txt")
test.setattributes('Year', 'Format')
operator = HashTable()
print()
print("put records into index")
for idx in range(len(test.record)):
    operator.Put(str(idx), test.record[idx])
print()
print("Find all DVD movies made in 1997")
temp = operator.Get("1997DVD")
for record in temp:
    print(record)
print()
print("Find all VHS movies made in 1990")
temp = operator.Get("1990VHS")
for record in temp:
    print(record)
print()
print("Find all DVD movies made in 2001")
temp = operator.Get("2001DVD")
for record in temp:
    print(record)
print()
print("Remove 2nd record from movie index")
operator.Remove("1")
print()
print("Find all DVD movies made in 2001")
temp = operator.Get("2001DVD")
for record in temp:
    print(record)


#  Test Case 2
print()
print('Test Case Two --- Set Year as Index')
test = ReadFile.ReadFile()
test.readFile("data.txt")
test.setattributes('Year')
operator = HashTable()
print()
print("put records into index")
for idx in range(len(test.record)):
    operator.Put(str(idx), test.record[idx])
print()
print("Find all movies made in 2000")
temp = operator.Get("2000")
for record in temp:
    print(record)
print()
print("Find all movies made in 2005")
temp = operator.Get("2005")
for record in temp:
    print(record)
print()
print("Find all movies made in 2010")
temp = operator.Get("2010")
for record in temp:
    print(record)
print()

