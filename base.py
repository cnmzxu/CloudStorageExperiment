import base64
import os
from hashlib import blake2b

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import myerrors

SALT = b'0123456789abcdef'

class EncSch:
    def __init__(self, keysize):
        self.keysize = keysize

    def Enc(self, key, plain):
        if len(key) != self.keysize:
            print("Key_Length_Error_Enc")
            raise myerrors.myerrors("Key_Length_Error_Enc")

        kdf =  PBKDF2HMAC(
                algorithm = hashes.SHA256(),
                length = 32,
                salt = SALT,
                iterations = 100000,
                backend = default_backend()
                )
        nnkey = base64.urlsafe_b64encode(kdf.derive(key))
        f = Fernet(nnkey)
        return f.encrypt(plain)

    def Dec(self, key, cipher):
        if len(key) != self.keysize:
            print("Key_Length_Error_Dec")
            raise myerrors.myerrors("Key_Length_Error_Dec")

        kdf =  PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = SALT,
            iterations = 100000,
            backend = default_backend()
            )
        nnkey = base64.urlsafe_b64encode(kdf.derive(key))
        f = Fernet(nnkey)
        try:
            return f.decrypt(cipher)
        except:
            print("Decrypt_Error")
            raise myerrors.myerrors("Decrypt_Error")

class Hash:
    def __init__(self, content = b"", bytesize = 64):
        self.bytesize = bytesize
        self.salts = [os.urandom(16) for i in range(bytesize // 64)]
        self.hashList = [blake2b(content, salt = s) for s in self.salts]
        if bytesize % 64 != 0:
            s = os.urandom(16)
            self.salts.append(s) 
            self.hashList.append(blake2b(content, digest_size = bytesize % 64, salt = s))

    def update(self, c):
        for hash in self.hashList:
            hash.update(c)
    
    def digest(self):
        h = b"".join([hash.digest() for hash in self.hashList])
        return h

    def hexdigest(self):
        h = b"".join([hash.hexdigest() for hash in self.hashList])
        return h

    def new(self, content = b""):
        if self.bytesize % 64 == 0:
            self.hashList = [blake2b(content, salt = s) for s in self.salts]
        else:
            self.hashList = [blake2b(content, salt = s) for s in self.salts[:-1]]
            self.hashList.append(blake2b(content, digest_size = self.bytesize % 64, salt = self.salts[-1]))

    def hash(self, content):
        self.new()
        self.update(content)
        return self.digest()
