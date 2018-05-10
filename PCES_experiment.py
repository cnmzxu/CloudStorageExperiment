import time
import shutil
import os

import PCES

repeat_time = 1

clienttime = 0
servertime = 0

try:
    os.remove("PCES_result.txt")
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
def exp1_func1(size, kappa, p):
    fresh()
    global clienttime, servertime
    CSS = PCES.PCES(kappa, p)
    for i in range(100):
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

def exp1_func2(size, kappa, p):
    st, ct = 0, 0
    for i in range(repeat_time):
        x = exp1_func1(size, kappa, p)
        st += x[0]
        ct += x[1]
    f = open("PCES_result.txt", "a")
    f.write("Average with kappa = %d, p = %f:\n" % (kappa, p))
    f.write("Server Time: %f\n" % (st / repeat_time))
    f.write("Client Time: %f\n" % (ct / repeat_time))
    f.close()

def exp1():
    f = open("PCES_result.txt", "a")
    f.write("Experiment1:\n")
    f.write("kappa = 512, p = 0.5:\n")
    f.close()
    for size in range(10, 28, 2):
        exp1_func2(size, 512, 0.5)
    
    f = open("PCES_result.txt", "a")
    f.write("size = 2^20 bytes, p = 0.5:\n")
    f.close()
    for kappa in [256, 512, 1024]:
        exp1_func2(20, kappa, 0.5)
    
    f = open("PCES_result.txt", "a")
    f.write("szie = 2 ^ 20 bytes, kappa = 512:\n")
    f.close()    
    for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        exp1_func2(20, 512, p)

"""
Upload 10 files of size 2^20 bytes 400 times for each one
count the servertime, clienttime amd deduplication rate.
"""
def exp2_func1(size, order, kappa, p):
    fresh()
    global clienttime, servertime
    CSS = PCES.PCES(kappa, p)
    for i in range(100):
        filename = 'ExperimentFiles/file_%d_%d' % (size, order)
        ufName = 'Uploads/file_%d_0_%d' % (size, i)
        uf = CSS.Upload(filename, ufName)
        CSS.Store(uf)    
    ciphernum = len(os.listdir("Uploads"))
    return ciphernum

def exp2_func2(size, kappa, p):
    st, ct, cn = 0, 0, 0
    for k in range (repeat_time):
        for i in range(10):
            x = exp2_func1(size, i, kappa, p)
            cn += x
    f = open("PCES_result.txt", "a")
    f.write("Average with size = 2^%d bytes, kappa = %d, p = %f\n" % (size, kappa, p))
    f.write("Ciphertext Num: %f\n" % (cn / repeat_time))
    f.close()

def exp2():
    f = open("PCES_result.txt", "a")
    f.write("Experiment2:\n")
    f.write("kappa = 512, p = 0.5:\n")
    f.close()
    for size in range(10, 28, 2):
        exp2_func2(size, 512, 0.5)
    
    f = open("PCES_result.txt", "a")
    f.write("size = 2^20 bytes, p = 0.5:\n")
    f.close()
    for kappa in [256, 512, 1024]:
        exp2_func2(20, kappa, 0.5)
    
    f = open("PCES_result.txt", "a")
    f.write("szie = 2 ^ 20 bytes, kappa = 512:\n")
    f.close()    
    for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        exp2_func2(20, 512, p)