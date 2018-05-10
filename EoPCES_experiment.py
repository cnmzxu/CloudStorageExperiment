import time
import shutil
import os

import EoPCES
import sssa

repeat_time = 1

clienttime = 0
servertime = 0

try:
    os.remove("EoPCES_result.txt")
except:
    None

def fresh():
    try:
        shutil.rmtree('Uploads')
    except:
        None
    try:
        shutil.rmtree('Plaintexts')
    except:
        None
    os.mkdir('Uploads')
    os.mkdir('Plaintexts')
    global clienttime, servertime
    clienttime = servertime = 0



"""
Experiment1:
For each size, upload 1 file for 400 times
count the time, number of cipher and plaintext
"""
def exp1_func1(size, kappa, p, sigma, th, PRIME):
    fresh()
    global clienttime, servertime
    CSS = EoPCES.EoPCES(kappa, p, sigma, th, PRIME)
    for i in range(400):
        filename = 'ExperimentFiles/file_%d_0' % size
        ufName = 'Uploads/file_%d_0_%d' % (size, i)
        t0 = time.clock()
        uf = CSS.Upload(filename, ufName)
        t1 = time.clock()
        CSS.Store(uf)
        t2 = time.clock()
        clienttime += t1 - t0
        servertime += t2 - t1
    return (servertime, clienttime)

def exp1_func2(size, kappa, p, sigma, th, PRIME):
    st, ct = 0, 0
    for i in range(repeat_time):
        x = exp1_func1(size, kappa, p, sigma, th, PRIME)
        st += x[0]
        ct += x[1]
    f = open("EoPCES_result.txt", "a")
    f.write("Average with size = 2^%d bytes, kappa = %d, p = %f, simga = %d, th = %d:\n" % (size, kappa, p, sigma, th))
    f.write("Server Time: %f\n" % (st / repeat_time))
    f.write("Client Time: %f\n" % (ct / repeat_time))
    f.close()

def exp1():
    f = open("EoPCES_result.txt", "a")
    f.write("Experiment1:\n")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for size in range(10, 28, 2):
        exp1_func2(size, 512, 0.5, 100, 20, sssa.PRIME2)

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for kappa in [(256, sssa.PRIME3), (512, sssa.PRIME2), (1024, sssa.PRIME1)]:
        exp1_func2(20, kappa[0], 0.5, 100, 20, kappa[1])

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        exp1_func2(20, 512, p, 100, 20, sssa.PRIME2)

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for sigma in range(50, 200, 10):
        exp1_func2(20, 512, 0.5, sigma, 20, sssa.PRIME2)

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for th in range(10, 40, 2):
        exp1_func2(20, 512, 0.5, 100, th, sssa.PRIME2)

"""
Upload 10 files of size 2^20 bytes 400 times for each one
count the servertime, clienttime amd deduplication rate.
"""
def exp2_func1(size, order, kappa, p, sigma, th, PRIME):
    fresh()
    global clienttime, servertime
    CSS = EoPCES.EoPCES(kappa, p, sigma, th, PRIME)
    for i in range(400):
        filename = 'ExperimentFiles/file_%d_%d' % (size, order)
        ufName = 'Uploads/file_%d_%d_%d' % (size, order, i)
        uf = CSS.Upload(filename, ufName)
        CSS.Store(uf)
    ciphernum = len(os.listdir("Uploads"))
    plainnum = len(os.listdir("Plaintexts"))
    return (ciphernum, plainnum)

def exp2_func2(size, kappa, p, sigma, th, PRIME):
    cn, pn = 0, 0
    for k in range (repeat_time):
        for i in range(10):
            x = exp2_func1(size, i, kappa, p, sigma, th, PRIME)
            cn += x[0]
            pn += x[1]
    f = open("EoPCES_result.txt", "a")
    f.write("Average with size = 2^%d bytes, kappa = %d, p = %f, sigma = %d, th = %d\n" % (size, kappa, p, sigma, th))
    f.write("Ciphertext Num: %f\n" % (cn / repeat_time))
    f.write("Plaintext Num: %f\n" % (pn / repeat_time))
    f.close()

def exp2():
    f = open("EoPCES_result.txt", "a")
    f.write("Experiment2:\n")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for size in range(10, 28, 2):
        exp2_func2(size, 512, 0.5, 100, 20, sssa.PRIME2)

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for kappa in [(256, sssa.PRIME3), (512, sssa.PRIME2), (1024, sssa.PRIME1)]:
        exp2_func2(20, kappa[0], 0.5, 100, 20, kappa[1])

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        exp2_func2(20, 512, p, 100, 20, sssa.PRIME2)

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for sigma in range(50, 200, 10):
        exp2_func2(20, 512, 0.5, sigma, 20, sssa.PRIME2)

    f = open("EoPCES_result.txt", "a")
    f.write("size = 2^20 bytes, kappa = 512, p = 0.5, sigma = 2^100, th = 20:\n")
    f.close()
    for th in range(10, 40, 2):
        exp2_func2(20, 512, 0.5, 100, th, sssa.PRIME2)