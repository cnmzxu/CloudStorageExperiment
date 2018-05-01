import time
import shutil
import os

import EoPCES
import sssa

repeat_time = 1

clienttime = 0
servertime = 0

f = open("EoPCES_result.txt", "w")

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
    ciphernum = len(os.listdir("Uploads"))
    plainnum = len(os.listdir("Plaintexts"))
    return (servertime, clienttime, ciphernum, plainnum)

def exp1_func2(size, kappa, p, sigma, th, PRIME):
    st, ct, cn, pn = 0, 0, 0, 0
    for i in range(repeat_time):
        x = exp1_func1(size, kappa, p, sigma, th, PRIME)
        st += x[0]
        ct += x[1]
        cn += x[2]
        pn += x[3]
    f.write("Average with kappa = %d, p = %f, simga = %d, th = %d:\n" % (kappa, p, sigma, th))
    f.write("Server Time: %f\n" % (st / repeat_time))
    f.write("Client Time: %f\n" % (ct / repeat_time))
    f.write("Ciphertext Num: %f\n" % (cn / repeat_time))
    f.write("Plaintext Num: %f\n" % (pn / repeat_time))

def exp1_func3(size):
    f.write("Experiment1 for 2^%d bytes file:\n" % size)
    exp1_func2(size, 1024, 0.5, 32, 20, sssa.PRIME1)

def exp1():
    f.write("Experiment1:\n")
    exp1_func3(10)
    exp1_func3(15)
    exp1_func3(20)
    exp1_func3(25)
    f.write("\n\n")

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
        t0 = time.clock()
        uf = CSS.Upload(filename, ufName)
        t1 = time.clock()
        CSS.Store(uf)
        t2 = time.clock()
        clienttime += t1 - t0
        servertime += t2 - t1
    
    ciphernum = len(os.listdir("Uploads"))
    plainnum = len(os.listdir("Plaintexts"))
    return (servertime, clienttime, ciphernum, plainnum)

def exp2_func2(size, kappa, p, sigma, th, PRIME):
    st, ct, cn, pn = 0, 0, 0, 0
    for k in range (repeat_time):
        for i in range(10):
            x = exp2_func1(size, i, kappa, p, sigma, th, PRIME)
            st += x[0]
            ct += x[1]
            cn += x[2]
            pn += x[3]
    f.write("Average with kappa = %d, p = %f, sigma = %d, th = %d\n" % (kappa, p, sigma, th))
    f.write("Server Time: %f\n" % (st / repeat_time))
    f.write("Client Time: %f\n" % (ct / repeat_time))
    f.write("Ciphertext Num: %f\n" % (cn / repeat_time))
    f.write("Plaintext Num: %f\n" % (pn / repeat_time))

def exp2_func3(size):
    """for kappa in [(256, sssa.PRIME3), (512, sssa.PRIME2), (1024, sssa.PRIME1)]:
        for p in [0.1, 0.5, 0.9]:
            for sigma in [50, 100, 200]:
                for th in [20, 40, 100]:
                    exp2_func2(size, kappa[0], p, sigma, th, kappa[1])"""
    exp2_func2(size, 256, 0.5, 100, 20, sssa.PRIME3)

def exp2():
    f.write("Experiment2:\n")
    exp2_func3(20)
#print("exp1")
#exp1()
print("exp2")
exp2()