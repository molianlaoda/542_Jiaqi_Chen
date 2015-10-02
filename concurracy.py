__author__ = 'jarfy'
import threading
from Operate_src import *
import MainBody
from timeit import Timer

global lock, client
count = 9
client = Operate_src("cs542.db")

lock = threading.Lock()

class client_thread(threading.Thread):
    def __init__(self, client_name, client_target, client_value = 0, client_action = "GET"):
        threading.Thread.__init__(self)
        self.client_name = client_name
        self.client_target = client_target
        self.client_value = client_value
        self.client_action = client_action

    def run(self):
        print self.client_name
        client_come_in(self.client_name, self.client_target, self.client_action, self.client_value)

def client_come_in(client_name, client_target, client_action="GET", client_value=0):
    global lock, client

    try:
        if client_action == "GET":                        #get action
            lock.acquire()
            print str(client_name) + " locks GET action"
            client.Get(client_target)
            print str(client_name) +" GETs lock released"
            lock.release()
        elif client_action == "PUT":                       #put action
            lock.acquire()
            print str(client_name) +" locks PUT action"
            client.Put(client_target, client_value)
            print str(client_name) +" PUTs lock released"
            lock.release()
            print "make sure put successfully" + str(client.db.keys())
        elif client_action == "RMV":                        #remove action
            lock.acquire()
            print str(client_name) +" locks RMV action"
            client.Remove(client_target)
            print str(client_name) +" RMVs lock released"
            lock.release()
            print "make sure remove successfully" + str(client.getdb.keys())
        else:
            raise AttributeError
    except AttributeError:
        print "there is no such action "
        return
