score = float(raw_input())
if score > 1 and score < 0:
    exit()
if score >= 0.9:
    print 'A'
elif score <0.8:
    print 'B'



'''import string

fhand = open('e.txt')
count = dict()

for line in fhand:
    operate = line.translate(None, string.punctuation)
    operate.lower()
    words = operate.split()
    for word in words:
        count[word] = count.get(word, 0) + 1

print count'''
