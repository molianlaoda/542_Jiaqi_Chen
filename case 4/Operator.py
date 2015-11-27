import MainBody
import os
import shutil
import random
from Logging import Logging

__author__ = 'Chan'


class Relation(object):
    city_path = 'data/City.txt'
    country_path = 'data/Country.txt'

    def __init__(self, data_path):
        self.data_path = data_path
        self.data = {}
        self.city = {}
        self.country = {}
        self.log = Logging()

    def open(self):
        #  If .db files exist, read them. If not, create them.
        if os.path.isfile(self.data_path):
            self.data = MainBody.fakeopen(self.data_path)
            try:
                del self.city
                del self.country
            except:
                pass

        else:
            self.data = MainBody.fakeopen(self.data_path)
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
                self.country[elm_list[0]] = [elm_list]

            self.data['city'] = self.city
            del self.city
            self.data['country'] = self.country
            del self.country
            self.data.sync()
        self.log.open()
        self.log.sync()

    def back_up(self, back_up_path):
        if os.path.isfile(back_up_path):
            print 'Back Up Already Exists. Aborted.'
            return
        try:
            shutil.copyfile(self.data_path, back_up_path)
            temp = MainBody.fakeopen(back_up_path)
            print temp['country']['ABW']
        except:
            print 'Back Up Failed!'
            return

    def auto_increase(self):
        cities = self.data['city']
        countries = self.data['country']
        for country_key in countries.keys():
            for country in countries[country_key]:
                old = country[6]
                country[6] = str(int(int(country[6]) * 1.02))
                self.log.record('country', country_key, 0, 6, old, country[6])
        for city_key in cities.keys():
            idx = 0
            for city in cities[city_key]:
                old = city[4]
                city[4] = str(int(int(city[4]) * 1.02))
                self.log.record('city', city_key, idx, 4, old, city[4])
                idx += 1
        self.data['city'] = cities
        self.data['country'] = countries
        self.data.sync()
        self.log.sync()

    def recover(self, back_up_path):
        backup = MainBody.fakeopen(back_up_path)
        self.log.recover(backup)
        print backup['country']
        backup.sync()
        backup.close()

    def close(self):
        self.data.close()
        self.log.close()

    def recover_show(self, relation):
        print 'randomly select content to show'
        countries = self.data['country'].keys()
        for i in range(0, 4):
            country = random.choice(countries)
            for j in self.log.log['records']:
                if j[0] == 'city' and j[1] == country and j[2] == 0:
                    print j[0], ' ', self.data['city'][country][0][1], ' old value is', j[4]
            print self.data['city'][country][0]


        #country
        for i in range(0, 4):
            print 'country'
            country = random.choice(countries)
            for j in self.log.log['records']:
                if j[0] == 'country' and j[1] == country and j[2] == 0:
                    print j[0], ' ', self.data['country'][country][0][1], ' old value is', j[4]
            print self.data['country'][country][0]

