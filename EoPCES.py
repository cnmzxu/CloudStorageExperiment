import random

import base

def PUD(n, h, p, sigma)
    if not 0 <= sigma <= n // 2:
        print("Sigma_Too_Large")
        raise myerror.myerror("Sigma_Too_Large")

    if not 0 <= h <= n - 1:
        print("H_Too_Large")
        raise myerror.myerror("H_Too_Large")
    
    f = random.uniform(0, 1)
    if f <= p:
        x = random.randint(h - sigma, h + sigma)
        if x < 0:
            return x + n
        else if x >= n:
            return x - n
        else:
            return x
    else:
        x = random.randint(h + sigma + 1, h + n - sigma - 1)
        if x < 0:
            return x + n
        else if x >= n:
            return x - n
        else:
            return x


def EoPCES:
    def __init__(self, kappa, p, sigma, th):
        self.kappa = kappa
        self.p = p
        self.sigma = sigma
        self.th = th
        self.__Enc__ = base.EncSch(kappa // 8).Enc
        self.__Dec__ = base.EncSch(kappa // 8).Dec
        self.__hash__ = base.Hash(bytesize = kappa // 4).hash

    def Upload(self, fileName, ufName):
        

    def Store(self, ufName, database, saveName):