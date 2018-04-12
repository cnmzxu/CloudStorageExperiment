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
    
    def Store(self, ufName, database, saveName):
        f = open(ufName, "rb")
        cipher = f.read()
        f.close()
        h = self.__hash__(cipher)
        if h not in database:
            database.add(h)
            f =open(saveName, "wb")
            f.write(cipher)
            return True
        else:
            return False
