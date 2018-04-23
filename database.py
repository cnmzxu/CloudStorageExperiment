import os
import random
import bisect

import sssa
import translation
import rbtree

class database:
    def __init__(self, kappa, th, sigma, DecryptFile, ss):
        """
        Make a segment tree.
        A node in this tree is a 3-list: [leftson, rightson, NumberOfuf]
        This tree at most has self.kappa layers
        """
        self.root = [None, None, 0]
        self.Dedup = rbtree.rbtree(lambda x:x[1]) #a value in Dedup is (hv1, hv2, F0_name)
        self.kappa = kappa
        self.FILTRATION = 2 ** kappa - 1
        self.DecryptFile = DecryptFile #(hv1, hv2, uf)
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
        mid = 1 << (self.kappa - 1)
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
            
    
    
    def add(self, uf): #return true: DB is changed, return flase otherwise
        """
        Add uf into the ufbase.If find more than self.th uf it do recovery, else do insert
        """
        s = self.Dedup.find_near(uf[0], self.sigma)
        for x in s:
            f0 = open(x[2])
            plain = f0.read()
            f0.close()
            f = self.DecryptFile(x[0], x[1], uf[2])
            if f == plain:
                return False
        self.insert(uf)
        return True


    def recovery(self, uf):
        bound = 2 ** self.sigma
        mid = uf[0]
        ub = mid + bound
        lb = mid - bound
        uploads = self.getUploads(lb, ub)
        minflag = min(uploads, key = lambda x: x[0])[0]
        maxflag = max(uploads, key = lambda x: x[0])[0]
        while True:
            if (self.count(minflag - bound, minflag + bound) >= self.th):
                update = self.getUploads(minflag - bound, minflag - 1)
                if (len(update) != 0):
                    minflag = min(update, key = lambda x: x[0])[0]
                    uploads = uploads + update
                else:
                    break
            else:
                break
        
        while True:
            if (self.count(maxflag - bound, maxflag + bound) >= self.th):
                update = self.getUploads(maxlag + 1, maxlag + bound)
                if (len(update) != 0):
                    maxlag = max(update, key = lambda x: x[0])[0]
                    uploads = uploads + update
                else:
                    break
            else:
                break

        if len(uploads) >= self.th:
            rightuploads = random.sample(uploads, self.th)
            secret = self.ss.recovery([x[1] for x in rightuploads])
            if secret[-16:] == '1' * 16
                print("Recovery Success.")
                upload = rightuploads[0]
                hv1 = secret[:self.kappa]
                hv2 = secret[self.kappa:2 * self.kappa]
                upfile = self.DecryptFile(hv1, hv2, upload[2])
                upfilename = 'Plaintexts/plain' + str(self.DecFileNum)
                self.DecFileNum += 1
                f = open(upfilename, 'wb')
                f.write(upfile)
                f.close()
                return (hv1, hv2, upfilename)

