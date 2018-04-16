import os
import random
import bisect

import sssa
import translation

class ufbase:
    def __init__(self, kappa, th, sigma, DecryptFile, ss):
        """
        Make a segment tree.
        A node in this tree is a 3-list: [leftson, rightson, NumberOfuf]
        This tree at most has self.kappa layers
        """
        self.root = [None, None, 0]
        self.deduplist = []
        self.flaglist = dict()
        self.kappa = kappa
        self.FILTRATION = 2 ** kappa - 1
        self.DecryptFile = DecryptFile
        self.th = th
        self.sigma = sigma
        self.ss = ss
        self.DecFileNum = 0

    def insert(self, uf):
        """
        This function inserts uf in the tree by flag value

        uf is a 3-tuple from client.OnceUpload.GetUploadFile and consists of 3 parts:
        flag: A int with self.kappa bits.
        secretShare: a tuple for secret sharing
        token: the encrypted file
        """
        mid = 2 ** (self.kappa - 1)
        flag = uf[0]
        layer = 0
        nownode = self.root
        while layer < self.kappa:
            nownode[2] += 1
            layer += 1
            if (flag < mid):
                if nownode[0] == None:
                    nownode[0] = [None, None, 0]
                nownode = nownode[0]
            else:
                if nownode[1] == None:
                    nownode[1] = [None, None, 0]
                nownode = nownode[1]
            flag = (flag << 1) & self.FILTRATION
        nownode[2] += 1
        nownode[0] = uf

    def __NodeCount(self, node, layer, lb, ub):
        """
        count number of uf in the tree with flag between lb and ub recursively
        
        lb and up are two int
        """
        if node == None or node[2] == 0:
            return 0
        if layer == self.kappa:
            return 1
      
        ubb = '1' * (self.kappa - layer) + '0' * layer
        if lb ==  0 and ub == int(ubb, 2):
            return node[2]
        
        mid = int('1' + '0' * (self.kappa - 1), 2)
        if lb < mid and ub < mid:
            return self.__NodeCount(node[0], layer + 1, lb << 1, ub << 1)
        elif lb >= mid and ub >= mid:
            return self.__NodeCount(node[1], layer + 1, (lb << 1) & self.FILTRATION, (ub << 1) & self.FILTRATION)
        else:
            return self.__NodeCount(node[0], layer + 1, (lb << 1) & self.FILTRATION, int('1' * (self.kappa - layer -1) + '0' * (layer + 1), 2)) + self.__NodeCount(node[1], layer + 1, 0, (ub << 1) & self.FILTRATION)



    def count(self, lowerbound, upperbound):
        mid = 2 ** self.kappa
        if lowerbound >= 0 and upperbound < mid:
            return self.__NodeCount(self.root, 0, lowerbound, upperbound)
        elif lowerbound < 0:
            return self.__NodeCount(self.root, 0, 0, upperbound) + self.__NodeCount(self.root, 0, lowerbound + mid, mid - 1)
        elif upperbound >= mid:
            return self.__NodeCount(self.root, 0, lowerbound, mid - 1) + self.__NodeCount(self.root, 0, 0, upperbound - mid)

    def __NodeGetUploads(self, node, layer, lb, ub):
        """
        Get uf whose flag is between lb and ub recursively.

        lb and ub are two ints
        """
        if node == None or node[2] == 0:
            return []
        if layer == self.kappa:
            return [node[0]]
        
        mid = 2 ** (self.kappa - 1)
        if lb < mid and ub < mid:
            return self.__NodeGetUploads(node[0], layer + 1, lb << 1, ub << 1)
        elif lb >= mid and ub >= mid:
            return self.__NodeGetUploads(node[1], layer + 1, (lb << 1) & self.FILTRATION, (ub << 1) & self.FILTRATION)
        else:
            return self.__NodeGetUploads(node[0], layer + 1, (lb << 1) & self.FILTRATION, int('1' * (self.kappa - layer -1) + '0' * (layer + 1), 2)) + self.__NodeGetUploads(node[1], layer + 1, 0, (ub << 1) & self.FILTRATION)


    def getUploads(self, lowerbound, upperbound):
        mid = 2 ** self.kappa
        if lowerbound >= 0 and upperbound < mid:
            return self.__NodeGetUploads(self.root, 0, lowerbound, upperbound)
        elif lowerbound < 0:
            return self.__NodeGetUploads(self.root, 0, 0, upperbound) + self.__NodeGetUploads(self.root, 0, lowerbound + mid, mid - 1)
        elif upperbound >= mid:
            return self.__NodeGetUploads(self.root, 0, lowerbound, mid - 1) + self.__NodeGetUploads(self.root, 0, 0, upperbound - mid)

    def __NodeDelete(self, node, layer, lb, ub, hv1, hv2, ofName):
        if node == None or node[2] == 0:
            return 0
        if layer == self.kappa:
            uf = node[0]
            token = self.DecryptFile(hv1, hv2, uf, ofName)
            f = open(ofName, 'rb')
            upfile = f.read()
            f.close()
            if token == upfile:
                os.remove(node[0][2])
                node[0] = None
                node[2] = 0
                return 0
            else:
                return node[2]

        mid = 2 ** (self.kappa - 1)
        if lb < mid and ub < mid:
            if node[1] == None:
                node[2] = 0
            else:
                node[2] = node[1][2]
            node[2] += self.__NodeDelete(node[0], layer + 1, lb << 1, ub << 1, hv1, hv2, ofName)
            return node[2]
        elif lb >= mid and ub >= mid:
            if node[0] == None:
                node[2] = 0
            else:
                node[2] = node[0][2]
            node[2] += self.__NodeDelete(node[1], layer + 1, (lb << 1) & self.FILTRATION, (ub << 1) & self.FILTRATION, hv1, hv2, ofName)
            return node[2]
        else:
            node[2] = self.__NodeDelete(node[0], layer + 1, (lb << 1) & self.FILTRATION, int('1' * (self.kappa - layer -1) + '0' * (layer + 1), 2), hv1, hv2, ofName) + self.__NodeDelete(node[1], layer + 1, 0, (ub << 1) & self.FILTRATION, hv1, hv2, ofName)
            return node[2]

    def delete(self, lowerbound, upperbound, key, flag, upfile):
        mid = 2 ** self.kappa
        if lowerbound >= 0 and upperbound < mid:
            self.__NodeDelete(self.root, 0, lowerbound, upperbound, key, flag, upfile)
        elif lowerbound < 0:
            self.__NodeDelete(self.root, 0, 0, upperbound, key, flag, upfile)
            self.__NodeDelete(self.root, 0, lowerbound + mid, mid - 1, key, flag, upfile)
        elif upperbound >= mid:
            self.__NodeDelete(self.root, 0, lowerbound, mid - 1, key, flag, upfile)
            self.__NodeDelete(self.root, 0, 0, upperbound - mid, key, flag, upfile)
            
        
    def recovery(self, mid):
        bound = 2 ** self.sigma
        ub = mid + bound
        lb = mid - bound
        uploads = self.getUploads(lb, ub)
        minlag = min(uploads, key = lambda x: x[0])[0]
        maxlag = max(uploads, key = lambda x: x[0])[0]
        while True:
            if (self.count(minlag - bound, minlag + bound) >= self.th):
                update = self.getUploads(minlag - bound, minlag - 1)
                if (len(update) != 0):
                    minlag = min(update, key = lambda x: x[0])[0]
                    uploads = uploads + update
                else:
                    break
            else:
                break
        
        while True:
            if (self.count(maxlag - bound, maxlag + bound) >= self.th):
                update = self.getUploads(maxlag + 1, maxlag + bound)
                if (len(update) != 0):
                    maxlag = max(update, key = lambda x: x[0])[0]
                    uploads = uploads + update
                else:
                    break
            else:
                break

        flag = 0
        if len(uploads) >= self.th:
            rightuploads = random.sample(uploads, self.th)
            secret = self.ss.recovery([x[1] for x in rightuploads])
            if secret[-6] == 255 and secret[-5] == 255 and secret[-4] == 255 and secret[-3] == 255 and secret[-2] == 255 and secret[-1] == 255:
                flag = 1

        if flag == 1:
            upload = rightuploads[0]
            key = bytes(secret[32:64])
            flag = translation.bytelist2int(secret[0:32])
            upfile = self.DecryptFile(key, (upload[0] - flag), upload[2])
            upfilename = 'Plaintexts/plain' + str(self.DecFileNum)
            self.DecFileNum += 1
            f = open(upfilename, 'wb')
            f.write(upfile)
            f.close()
            bisect.insort(self.deduplist, flag)
            self.flaglist[flag] = (key, upfilename)
            self.delete(lb, ub, key, flag, upfilename)
            return 1
        else:
            return 0

            


    def add(self, uf):
        """
        Add uf into the ufbase.If find more than self.th uf it do recovery, else do insert
        """
        mid = 2 ** self.kappa
        bound = 2 ** self.sigma
        flag = uf[0]
        if len(self.deduplist) > 0:
            for flag1 in self.deduplist:
                if abs(flag - flag1) <= bound or (mid - abs(flag - flag1)) <= bound:
                    ddd = self.flaglist[flag1]
                    token1 = self.DecryptFile(ddd[0], flag - flag1, uf[2])
                    f = open(ddd[1], 'rb')
                    token2 = f.read()
                    f.close()
                    if token1 == token2:
                        os.remove(uf[2])
                        return
                
        lb = flag - bound
        ub = flag + bound
        flag = 0
        if self.count(lb, ub) > self.th:
            flag = self.recovery(flag)
        if flag == 0:
            self.insert(uf)
