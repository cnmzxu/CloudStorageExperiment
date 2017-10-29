import base64
import os
import random
import bisect
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sssa
import translation
import client
import log

HASHLENGTH= 256
SIGMA = 64
PTHRESHOLD = 0.8
THRESHOLD = 20
FILTRATION = 2 ** HASHLENGTH - 1
pickTime = 10

DecFileNum = 0

def setParameter(sigma, p, thre, pt):
    global SIGMA, PTHRESHOLD, THRESHOLD, pickTime
    SIGMA, PTHRESHOLD, THRESHOLD, pickTime = sigma, p, thre, pt


class DataBase:
    def __init__(self):
        """
        Make a segment tree.
        A node in this tree is a 4-list: [leftson, rightson, NumberOfData]
        This tree has HASHLENGTH layers

        """
        self.root = [None, None, 0, 1]
        self.deduplist = []
        self.laglist = dict()

    def insert(self, data):
        """
        This function inserts data in the tree by lag value

        data is a 3-tuple from client.OnceUpload.GetUploadFile and consists of 3 parts:
        lag: A int with HASHLENGTH bits.
        secretShare: a tuple for secret sharing
        token: the encrypted file
        """
        limit = 2 ** (HASHLENGTH - 1)
        lag = data[0]
        layer = 0
        nownode = self.root
        while layer < HASHLENGTH:
            nownode[2] += 1
            layer += 1
            if (lag < limit):
                if nownode[0] == None:
                    nownode[0] = [None, None, 0]
                nownode = nownode[0]
            else:
                if nownode[1] == None:
                    nownode[1] = [None, None, 0]
                nownode = nownode[1]
            lag = (lag << 1) & FILTRATION
        nownode[2] += 1
        nownode[0] = data

    def __NodeCount(self, node, layer, lb, ub):
        """
        count number of data in the tree with lag between lb and ub recursively

        lb and up are two int
        """
        if node == None or node[2] == 0:
            return 0
        if layer == HASHLENGTH:
            return 1
      
        ubb = '1' * (HASHLENGTH - layer) + '0' * layer
        if lb ==  0 and ub == int(ubb, 2):
            return node[2]
        
        limit = int('1' + '0' * (HASHLENGTH - 1), 2)
        if lb < limit and ub < limit:
            return self.__NodeCount(node[0], layer + 1, lb << 1, ub << 1)
        elif lb >= limit and ub >= limit:
            return self.__NodeCount(node[1], layer + 1, (lb << 1) & FILTRATION, (ub << 1) & FILTRATION)
        else:
            return self.__NodeCount(node[0], layer + 1, (lb << 1) & FILTRATION, int('1' * (HASHLENGTH - layer -1) + '0' * (layer + 1), 2)) + self.__NodeCount(node[1], layer + 1, 0, (ub << 1) & FILTRATION)



    def count(self, lowerbound, upperbound):
        limit = 2 ** HASHLENGTH
        if lowerbound >= 0 and upperbound < limit:
            return self.__NodeCount(self.root, 0, lowerbound, upperbound)
        elif lowerbound < 0:
            return self.__NodeCount(self.root, 0, 0, upperbound) + self.__NodeCount(self.root, 0, lowerbound + limit, limit - 1)
        elif upperbound >= limit:
            return self.__NodeCount(self.root, 0, lowerbound, limit - 1) + self.__NodeCount(self.root, 0, 0, upperbound - limit)

    def __NodeGetUploads(self, node, layer, lb, ub):
        """
        Get data whose lag is between lb and ub recursively.

        lb and ub are two ints
        """
        if node == None or node[2] == 0:
            return []
        if layer == HASHLENGTH:
            return [node[0]]
        
        limit = 2 ** (HASHLENGTH - 1)
        if lb < limit and ub < limit:
            return self.__NodeGetUploads(node[0], layer + 1, lb << 1, ub << 1)
        elif lb >= limit and ub >= limit:
            return self.__NodeGetUploads(node[1], layer + 1, (lb << 1) & FILTRATION, (ub << 1) & FILTRATION)
        else:
            return self.__NodeGetUploads(node[0], layer + 1, (lb << 1) & FILTRATION, int('1' * (HASHLENGTH - layer -1) + '0' * (layer + 1), 2)) + self.__NodeGetUploads(node[1], layer + 1, 0, (ub << 1) & FILTRATION)


    def getUploads(self, lowerbound, upperbound):
        limit = 2 ** HASHLENGTH
        if lowerbound >= 0 and upperbound < limit:
            return self.__NodeGetUploads(self.root, 0, lowerbound, upperbound)
        elif lowerbound < 0:
            return self.__NodeGetUploads(self.root, 0, 0, upperbound) + self.__NodeGetUploads(self.root, 0, lowerbound + limit, limit - 1)
        elif upperbound >= limit:
            return self.__NodeGetUploads(self.root, 0, lowerbound, limit - 1) + self.__NodeGetUploads(self.root, 0, 0, upperbound - limit)

    def __NodeDelete(self, node, layer, lb, ub, key, lag, upfilename):
        if node == None or node[2] == 0:
            return 0
        if layer == HASHLENGTH:
            data = node[0]
            token = client.DecryptFile(key, (data[0] - lag), data[2])
            f = open(upfilename, 'rb')
            upfile = f.read()
            f.close()
            if token == upfile:
                os.remove(node[0][2])
                #log.Log().serverlog("delete %s -> %s\n" % (node[0][2], upfilename))
                node[0] = None
                node[2] = 0
                return 0
            else:
                return node[2]

        limit = 2 ** (HASHLENGTH - 1)
        if lb < limit and ub < limit:
            if node[1] == None:
                node[2] = 0
            else:
                node[2] = node[1][2]
            node[2] += self.__NodeDelete(node[0], layer + 1, lb << 1, ub << 1, key, lag, upfilename)
            return node[2]

        elif lb >= limit and ub >= limit:
            if node[0] == None:
                node[2] = 0
            else:
                node[2] = node[0][2]
            node[2] += self.__NodeDelete(node[1], layer + 1, (lb << 1) & FILTRATION, (ub << 1) & FILTRATION, key, lag, upfilename)
            return node[2]
        else:
            node[2] = self.__NodeDelete(node[0], layer + 1, (lb << 1) & FILTRATION, int('1' * (HASHLENGTH - layer -1) + '0' * (layer + 1), 2), key, lag, upfilename) + self.__NodeDelete(node[1], layer + 1, 0, (ub << 1) & FILTRATION, key, lag, upfilename)
            return node[2]

    def delete(self, lowerbound, upperbound, key, lag, upfile):
        limit = 2 ** HASHLENGTH
        if lowerbound >= 0 and upperbound < limit:
            self.__NodeDelete(self.root, 0, lowerbound, upperbound, key, lag, upfile)
        elif lowerbound < 0:
            self.__NodeDelete(self.root, 0, 0, upperbound, key, lag, upfile)
            self.__NodeDelete(self.root, 0, lowerbound + limit, limit - 1, key, lag, upfile)
        elif upperbound >= limit:
            self.__NodeDelete(self.root, 0, lowerbound, limit - 1, key, lag, upfile)
            self.__NodeDelete(self.root, 0, 0, upperbound - limit, key, lag, upfile)
            
        
    def recovery(self, mid):
        bound = 2 ** SIGMA
        ub = mid + bound
        lb = mid - bound
        uploads = self.getUploads(lb, ub)
        minlag = min(uploads, key = lambda x: x[0])[0]
        maxlag = max(uploads, key = lambda x: x[0])[0]
        while True:
            if (self.count(minlag - bound, minlag + bound) >= THRESHOLD):
                update = self.getUploads(minlag - bound, minlag - 1)
                if (len(update) != 0):
                    minlag = min(update, key = lambda x: x[0])[0]
                    uploads = uploads + update
                else:
                    break
            else:
                break
        
        while True:
            if (self.count(maxlag - bound, maxlag + bound) >= THRESHOLD):
                update = self.getUploads(maxlag + 1, maxlag + bound)
                if (len(update) != 0):
                    maxlag = max(update, key = lambda x: x[0])[0]
                    uploads = uploads + update
                else:
                    break
            else:
                break

        flag = 0
        ss = sssa.sssa(THRESHOLD, HASHLENGTH // 4 + 6) 
        for i in range(pickTime):
            rightuploads = random.sample(uploads, THRESHOLD)
            secret = ss.recovery([x[1] for x in rightuploads])
            if secret[-6] == 255 and secret[-5] == 255 and secret[-4] == 255 and secret[-3] == 255 and secret[-2] == 255 and secret[-1] == 255:
                flag = 1
                break

        if flag == 1:
            upload = rightuploads[0]
            key = bytes(secret[32:64])
            lag = translation.bytelist2int(secret[0:32])
            upfile = client.DecryptFile(key, (upload[0] - lag), upload[2])
            global DecFileNum
            upfilename = 'Plaintexts/plain' + str(DecFileNum)
            DecFileNum += 1
            f = open(upfilename, 'wb')
            f.write(upfile)
            f.close()
            bisect.insort(self.deduplist, lag)
            self.laglist[lag] = (key, upfilename)
            self.delete(lb, ub, key, lag, upfilename)
            return 1
        else:
            return 0

            


    def add(self, data):
        """
        Add data into the database.If find more than THRESHOLD data it do recovery, else do insert
        """
        limit = 2 ** HASHLENGTH
        bound = 2 ** SIGMA
        lag = data[0]
        #log.Log().serverlog("Get file %s:\n" % data[2])###############
        #log.Log().serverlog("Lag: %d\n\n" % lag)##########
        if len(self.deduplist) > 0:
            for lag1 in self.deduplist:
                if abs(lag - lag1) <= bound or (limit - abs(lag - lag1)) <= bound:
                    ddd = self.laglist[lag1]
                    token1 = client.DecryptFile(ddd[0], lag - lag1, data[2])
                    f = open(ddd[1], 'rb')
                    token2 = f.read()
                    f.close()
                    if token1 == token2:
                        os.remove(data[2])
                        #log.Log().serverlog("delete %s -> %s\n\n" % (data[2], ddd[1]))################
                        return
                
        lb = lag - bound
        ub = lag + bound
        flag = 0
        if self.count(lb, ub) > THRESHOLD:
            flag = self.recovery(lag)
        if flag == 0:
            self.insert(data)
