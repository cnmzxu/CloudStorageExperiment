import random
import os

import base
import database
import translation
import myerror
import sssa

def PUD(n, h, p, sigma, f):
    if f <= p:
        x = random.randint(h - sigma, h + sigma)
        if x < 0:
            return x + n
        elif x >= n:
            return x - n
        else:
            return x
    else:
        x = random.randint(h + sigma + 1, h + n - sigma - 1)
        if x < 0:
            return x + n
        elif x >= n:
            return x - n
        else:
            return x

def __DecryptFile__(kappa, __Dec__):
    def __Function__(hv1, hv2, uf):
        x = (uf[0] - int(hv2, 2)) % 2 ** kappa
        key = hv1 + bin(x)[2:].zfill(kappa)[:kappa]
        key = translation.bin2bytelist(key)
        f = open(uf[2], "rb")
        cipher = f.read()
        f.close()
        plain = __Dec__(key, cipher)
        return plain
    return __Function__

class EoPCES:
    def __init__(self, kappa, p, sigma, th, PRIME):#sigma : number of bits
        if sigma > kappa:
            raise myerror.myerror("Sigma_Larger_Than_Kappa")
        self.kappa = kappa
        self.p = p
        self.sigma = 2 ** sigma
        self.th = th
        self.__Enc__ = base.EncSch(kappa // 4).Enc
        self.__Dec__ = base.EncSch(kappa // 4).Dec
        self.__hash__ = base.Hash(bytesize = kappa // 4).hash
        self.__ss__ = sssa.sssa(th, 2 * kappa + 16, PRIME)
        self.DB = database.database(kappa, th, sigma, __DecryptFile__(kappa, self.__Dec__), self.__ss__)

    def Upload(self, fileName, ufName):
        f = open(fileName, "rb")
        content = f.read()
        hv = translation.bytelist2bin(self.__hash__(content))[:2 * self.kappa].zfill(2 * self.kappa)
        hv2 = hv[self.kappa:2 * self.kappa]
        f = random.uniform(0, 1)
        x = PUD(2**self.kappa, 0, self.p, self.sigma, f)
        if f <= self.p:
            hv1 = hv[:self.kappa].zfill(self.kappa)
            sh = self.__ss__.share(hv + '1' * 16)
        else:
            hv1 = translation.bytelist2bin(os.urandom(self.kappa // 8))[:self.kappa]
            s = translation.bytelist2bin(os.urandom(self.kappa // 4))[:2 * self.kappa]
            sh = self.__ss__.share(s + '1' * 16)
        key = hv1 + bin(x)[2:self.kappa + 2].zfill(self.kappa)
        key = translation.bin2bytelist(key)
        C = self.__Enc__(key, content)
        key = (hv1, x)
        flag = (int(hv2, 2) + x) % 2**self.kappa
        f = open(ufName, "wb")
        f.write(C)
        f.close()
        return (flag, sh, ufName, key)

    def Store(self, uf):
        if self.DB.add(uf):
            result = self.DB.recovery(uf[0])
            if result != None:
                self.DB.deduplication(result)

def test():
    server = EoPCES(1024, 1, 32, 20, sssa.PRIME1)
    for i in range(30):
        print(i)
        uf = server.Upload("test.py", "Uploads/uploadfile" + str(i))
        server.Store(uf)

#test()