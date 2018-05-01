import base64
import os
import random
import time
from hashlib import blake2b

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
f = open("test.py", "rb")
plain = f.read()
f.close()
key = b"adsfasdf"
kdf =  PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = b"asdfasdf", 
        iterations = 100000,
        backend = default_backend()
        )
key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor1 = cipher.encryptor()
encryptor2 = cipher.encryptor()
ct = encryptor1.update(b"a secret message")
print(encryptor1.update(b"a secret message"))
print(encryptor2.update(b"a secret message"))
decryptor = cipher.decryptor()
decryptor.update(ct)