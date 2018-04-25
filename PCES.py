import os
import random

import base


class PCES:
    def __init__(self, kappa, p):
        self.kappa = kappa
        self.p = p
        self.__Enc__ = base.EncSch(kappa // 8).Enc
        self.__Dec__ = base.EncSch(kappa // 8).Dec
        self.__hash__ = base.Hash(bytesize = kappa // 8).hash
        self.database = set()
    
    def Upload(self, fileName, ufName):
        f = open(fileName, "rb")
        content = f.read()
        f.close()
        f = random.uniform(0, 1)
        
        if f <= self.p:
            key = self.__hash__(content)
        else:
            key = os.urandom(self.kappa // 8)
        
        cipher = self.__Enc__(key, content)
        f = open(ufName, "wb")
        f.write(cipher)
        f.close()
        h = self.__hash__(cipher)
        return (h, ufName)
    
    def Store(self, uf):
        h = uf[0]
        if h not in self.database:
            self.database.add(h)
            return True
        else:
            os.remove(uf[1])
            return False
