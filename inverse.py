import random
import datetime

def inverse1(a, b):
    if a == 1:
        return 1
    
    b_ = b % a
    y = inverse1(b_, a)
    return (-b * y + 1) // a

def inverse2(a, b):
    exp = b - 2
    w = a
    ans = 1
    while exp > 0:
        if exp & 1 == 1:
            ans = (ans * w) % b
        w = (w ** 2) % b
        exp = exp >> 1
    return ans


P = 8925104775867795951373020225107048318661262697096153964432239415414187036173666062582256743654902410429508634182852333827388328617160062696400712196543187
begin = datetime.datetime.now()
for i in range(10000):
    a = random.randint(0, P - 1)
    if (a * inverse1(a, P)) % P != 1:
        print(False)
end = datetime.datetime.now()
print("1 : ", end - begin)

begin = datetime.datetime.now()
for i in range(10000):
    a = random.randint(0, P - 1)
    if (a * inverse2(a, P)) % P != 1:
        print(False)
end = datetime.datetime.now()
print("2 : ", end - begin)