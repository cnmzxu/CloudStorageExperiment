import time
import shutil
import os

import PCES

repeat_time = 1

clienttime = 0
servertime = 0

f = open("result.txt", "w")

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
    CSS = PCES.PCES(kappa, p)
    for i in range(400):
        filename = 'ExperimentFiles/file_%d_0' % size
        ufName = 'Uploads/file_%d_0_%d' % (size, i)
        t0 = time.clock()
        uf = CSS.Upload(filename, ufName)
        t1 = time.clock()
        CSS.Store(uf)
        t2 = time.clock()
        global clienttime, servertime
        clienttime += t1 - t0
        servertime += t2 - t1
    ciphernum = len(os.listdir("Uploads"))
    plainnum = len(os.listdir("Plaintexts"))
    return (servertime, clienttime, ciphernum, plainnum)

def exp1_func2(size, kappa, p):
    st, ct, cn, pn = 0, 0, 0, 0
    for i in range(repeat_time):
        x = exp1_func1(size, kappa, p)
        st += x[0]
        ct += x[1]
        cn += x[2]
        pn += x[3]
    f.write("Average with kappa = %d, p = %f:\n" % (kappa, p))
    f.write("Server Time: %f\n" % (st / repeat_time))
    f.write("Client Time: %f\n" % (ct / repeat_time))
    f.write("Ciphertext Num: %f\n" % (cn / repeat_time))
    f.write("Plaintext Num: %f\n\n" % (pn / repeat_time))

def exp1_func3(size):
    f.write("Experiment1 for 2^%d bytes file:\n" % size)
    exp1_func2(size, 1024, 0.5)



def exp1():
    f.write("Experiment1:\n")
    exp1_func3(10)
    exp1_func3(15)
    exp1_func3(20)
    exp1_func3(25)
    f.write("\n\n")

exp1()