import random
import translation

PRIME1 =2245266068043787735525206115268156717978410543431742073158779754074807191429634511625933785398904267375520986004146836085924054353942453992058345333433211890887378663767033 #70 bytes


def getInverse(k):
    if k > PRIME1:
        print("Cannot get inverse.")
        return None
    exponent = PRIME1 - 2
    w = k % PRIME1
    ans = 1
    while exponent > 0:
        if exponent & 0x1 == 1:
            ans = (ans * w) % PRIME1
        w = (w ** 2) % PRIME1
        exponent = exponent >> 1
    return ans

class sssa:
    def __init__(self, thre, bytelength):
        self.threshold = thre
        self.moudle = PRIME1
        self.bytelength = bytelength

    def share(self, bytelist):
        if (len(bytelist) != self.bytelength):
            print("No matchable bytelist.")
            return None 
        secret = translation.bytelist2int(bytelist)
        uid = random.randint(1, PRIME1 - 1)
        ans = 0
        for i in range(self.threshold - 1):
            ans = (ans * uid + bytelist[i]) % PRIME1
        ans = (ans * uid + secret) % PRIME1
        return (uid, ans)

    def recovery(self, shares):
        if (len(shares) != self.threshold):
            print("No enough secret shares.")
            raise NotEnoughSharesError
        ans = {}
        secret = 0
        for i in range(self.threshold):
            w = shares[i][1]
            xi = shares[i][0]
            for j in range(self.threshold):
                if (j != i):
                    xj = shares[j][0]
                    w = (((xj * getInverse(xj - xi)) % PRIME1) * w) % PRIME1
            secret = (secret + w) % PRIME1
        return list(translation.int2bytelist(secret, self.bytelength))
     

