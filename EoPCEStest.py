from EoPCES import EoPCES
import sssa
import translation

import os

s = EoPCES(256, 0.8, 64, 10, sssa.PRIME2)

key = s.Upload("test.py", "upload/cipher1.txt")[3]
f = open("upload/cipher1.txt", "rb")
cipher = f.read()
f.close()
k = key[0] + bin(key[1])[2:258].zfill(256)
key = translation.bin2bytelist(k)
plain = s.__Dec__(key, cipher)
f = open("upload/plain1.txt", "wb")
f.write(plain)
f.close



