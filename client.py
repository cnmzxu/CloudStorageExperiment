import base64
import os
import random
import sssa
import translation
import log

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HASHLENGTH= 256
SIGMA = 64
PTHRESHOLD = 0.8
THRESHOLD = 20
SALT = b'0123456789abcdef'

UploadedFileNumber = 0

def setParameter(sigma, p, thre):
    global SIGMA, PTHRESHOLD, THRESHOLD
    SIGMA, PTHRESHOLD, THRESHOLD = sigma, p, thre

class OnceUpload:
    def __randbyte(self, flag):
        """
            get a random byte string of hashlength
            flag = 0 return < 2^sigma
            flag = 1 return >= 2^sigma
            left is big end
            right is little end
        """
        bound1 = 2 ** SIGMA - 1
        bound2 = 2 ** HASHLENGTH - 1
        if flag == 0:
            return random.randint(-bound1, bound1)
        else:                
            return random.choice([-1, 1]) * random.randint(bound1, bound2)

    def __init__(self, upfilename):
        upfile = open(upfilename, 'rb')
        filecontent = upfile.read()
        upfile.close()
        self.randbytes = None
        p = random.uniform(0, 1)
        if p < PTHRESHOLD:
            flag = 0
        else:
            flag = 1
        self.randbytes = self.__randbyte(flag)

        hashfunction = hashes.Hash(hashes.SHA512(), backend = default_backend()) 
        hashfunction.update(filecontent)
        self.hv512 = list(hashfunction.finalize())
        hashlag = self.hv512[0:32]
        self.lag = translation.bytelist2int(hashlag)
        
        self.lag = (self.lag + self.randbytes) % int('1'+ '0' * HASHLENGTH, 2)

        self.key = bytes(self.hv512[32:64])

        kdf =  PBKDF2HMAC(
                algorithm = hashes.SHA256(),
                length = 32,
                salt = SALT,
                iterations = 100000,
                backend = default_backend()
                )
        nnkey = base64.urlsafe_b64encode(kdf.derive(self.key + translation.int2bytelist(self.randbytes % int('1' + '0' * HASHLENGTH, 2), HASHLENGTH // 8)))
        f = Fernet(nnkey)
        token = f.encrypt(filecontent)
        global UploadedFileNumber
        self.ciphername = "Ciphertexts/cipher" + str(UploadedFileNumber)
        UploadedFileNumber += 1
        f = open(self.ciphername, 'wb')
        f.write(token)
        f.close()
        #log.Log().clientlog(upfilename, flag, self.ciphername, self.hv512, self.lag, self.key, self.randbytes)

    def GetUploadFile(self):
        ss = sssa.sssa(THRESHOLD, HASHLENGTH // 4 + 6) 
        return (self.lag, ss.share(self.hv512 + [255] * 6), self.ciphername)

    def GetKeys(self):
        return (self.key, self.randbytes)

def DecryptFile(key, randbytes, ciphername):
    kdf =  PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = SALT,
            iterations = 100000,
            backend = default_backend()
            )
    nnkey = base64.urlsafe_b64encode(kdf.derive(key + translation.int2bytelist(randbytes % int('1' + '0' * HASHLENGTH, 2), HASHLENGTH // 8)))
    k = Fernet(nnkey)
    f = open(ciphername, 'rb')
    upfile = k.decrypt(f.read())
    f.close()
    return upfile

