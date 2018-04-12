import random
import translation

#2048 bits
PRIME1 = 26642305782553640600499410180168648140267981411862303823499017191536095889810897282774584920941184577953410850892419387312100349041117977412804559664196851385173233392880160689581774405432726466773745408164357833019937100917934662168984014161212910733789126921943450792163397814199345779743675468852056897996039819007412606419971702843391482131914974971926911205759486195362130292136408385973317330521698136207368628261315066110721871439076776015308601831609285240688643849928446221553693051463152830431220562303895376224075936309374285806425591314600877626968622957251094470642538236416045579460026371416755108118429

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
    def __init__(self, th, length):
        self.threshold = thre
        self.moudle = PRIME1
        self.length = length

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
     

print(PRIME1)