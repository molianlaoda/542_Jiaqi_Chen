import MainBody
import concurracy
from timeit import Timer

test = MainBody.fakeopen('cs542.db')
print 'Puting "A" in'
print 'Size: 1048000 Bytes'
test['A'] = bytearray(1048000)
test.sync()
print 'Puting "B" in'
print 'Size: 1048000 Bytes'
test['B'] = bytearray(1048000)
test.sync()
print 'Puting "C" in'
print 'Size: 1048000 Bytes'
test['C'] = bytearray(1048000)
test.sync()
print 'Puting "D" in'
print 'Size: 1048000 Bytes'
test['D'] = bytearray(1048000)
test.sync()
print 'Deleting "B"'
del test['B']
print 'Puting "E" in'
print 'Size: 1048000/2 Bytes'
test['E'] = bytearray(1048000/2)
print 'Puting "F" in'
print 'Size: 1048000 Bytes'
test['F'] = bytearray(1048000)
test.sync()
del test['C']
print 'Deleting "C"'
print 'Puting "G" in'
print 'Size: 1048000 Bytes'
test['G'] = bytearray(1048000)
test.sync()
print 'Deleting "E"'
del test['E']
print 'Puting "H" in'
print 'Size: 1048000 Bytes'
test['H'] = bytearray(1048000)
test.sync()
for key in test.keys():
    if key != 'metadata':
        print str(key)+ ": " + str(test.getMeta(key))
test.clearall()
test.close()

thread3 = concurracy.client_thread("RMV-client 3", "R", client_action="RMV")
thread1 = concurracy.client_thread("PUT-client 1", "R", client_action="PUT", client_value=1048000)
thread2 = concurracy.client_thread("GET-client 2", "R", client_action="GET")
thread4 = concurracy.client_thread("RMV-client 4", "R", client_action="RMV")

print "----------------------------------------"

print "start concurracy"
def start_thread():
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

start_thread()
