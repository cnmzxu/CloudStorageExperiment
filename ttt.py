import datetime
import random

x1 = random.randint(0, 10)
y1 = random.randint(0, 10)
x2 = random.randint(0, 1 << 2048)
y2 = random.randint(0, 1 << 2048)

t1 = datetime.datetime.now()
for i in range(1000000):
    b1 = (x1 <= y1)
t2 = datetime.datetime.now()
print(t2 - t1)

t1 = datetime.datetime.now()
for i in range(10000):
    b1 = (x2 <= y2)
t2 = datetime.datetime.now()
print(t2 - t1)