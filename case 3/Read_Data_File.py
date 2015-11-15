__author__ = 'Jiaqi'
import MainBody
import os
from prettytable import PrettyTable


class Relation():

    city_path = 'data/City.txt'
    country_path = 'data/Country.txt'

    def __init__(self):
        self.city = {}
        self.country = {}

    def open(self):
        #  If .db files exist, read them. If not, create them.
        if os.path.isfile('data/City.db') and os.path.isfile('data/Country.db'):
            print 'The pipeline has been opened!'
            self.city = MainBody.fakeopen('data/City.db')
            self.country = MainBody.fakeopen('data/Country.db')

        else:
            print "Have to create db files! Don't panic!"
            print "The pipeline has been opened!"
            self.city = MainBody.fakeopen('data/City.db')
            self.country = MainBody.fakeopen('data/Country.db')
            city_handle = open(self.city_path, 'r')
            country_handle = open(self.country_path, 'r')
            for city in city_handle:
                elm_list = city.split('\t')
                try:
                    self.city[elm_list[2]].append(elm_list)
                except:
                    self.city[elm_list[2]] = [elm_list]

            for country in country_handle:
                elm_list = country.split('\t')
                self.country[elm_list[0]] = elm_list

            self.country.sync()
            self.city.sync()

    def getNext(self):
        big_cities = {}
        country_list = self.country.values()
        for each_country in country_list:
            if type(each_country) == type({}):
                continue
            country_population = each_country[6]
            country_code = each_country[0]
            if country_population == '0':
                continue
            cities_of_country = self.city[country_code]
            cities = [] #store cities whose population have more than 40%national population
            for each_city in cities_of_country:
                city_population = each_city[4]
                if each_city[3] == '\xc2\x96':
                    each_city[3] = 'No record'
                if city_population == '0':
                    continue
                if float(city_population) > float(country_population) * 0.4:
                    cities.append(each_city)
                    big_cities[country_code] = cities

        return big_cities

    def close(self):
        print "The pipeline has been closed!"
        self.city.close()
        self.country.close()

test = Relation()
test.open()
cities = test.getNext()
test.close()
# print cities
print
print 'Population of city is more than 40% of the national populaion of the city: '
table = PrettyTable(["ID", "City name", "Country code", "District", "Population"])
table.padding_width = 1
for i in cities:
    country = cities[i]
    for j in country:
        table.add_row(j)
print table