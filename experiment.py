import os
import sys
import shutil
import client
import server
import time

f = open("explog.txt", 'w')

def fresh():
    try:
        os.remove("clog.txt")
    except:
        None
    
    try:
        os.remove("slog.txt")
    except:
        None
    
    try:
        shutil.rmtree("Ciphertexts")
    except:
        None
    
    try:
        shutil.rmtree("Plaintexts")
    except:
        None

    os.mkdir("Ciphertexts")
    os.mkdir("Plaintexts")

"""
Experiment1:
For each size, upload 1 file for 400 times
count the time, number of cipher and plaintext
"""
retime = 1
def exp1_func1(size, s, p, t):
    fresh()
    server.setParameter(s, p, t, 1)
    client.setParameter(s, p, t)
    db = server.DataBase()
    clienttime = 0
    servertime = 0
    for i in range(200):
        filename = 'ExperimentFiles/file_%d_0' % size
        t0 = time.time()
        up = client.OnceUpload(filename)
        xx = up.GetUploadFile()
        t1 = time.time()
        db.add(xx)
        t2 = time.time()
        clienttime += t1 - t0
        servertime += t2 - t1
    
    ciphernum = len(os.listdir("Ciphertexts"))
    plainnum = len(os.listdir("Plaintexts"))
    """f.write("Experiment 1 for 2^%d bytes:\n" % size)
    f.write("Server Time: %f\n" % servertime)
    f.write("Client Time: %f\n" % clienttime)
    f.write("Ciphertext Num: %d\n" % ciphernum)
    f.write("Plaintext Num: %d\n\n" % plainnum)"""
    return (servertime, clienttime, ciphernum, plainnum)

def exp1_func2(size, s, p, t):
    st, ct, cn, pn = 0, 0, 0, 0
    for i in range(retime):
        x = exp1_func1(size, s, p, t)
        st += x[0]
        ct += x[1]
        cn += x[2]
        pn += x[3]
    f.write("Average with sigma = %d, p = %f, threshold = %d:\n" % (s, p, t))
    f.write("Server Time: %f\n" % (st / retime))
    f.write("Client Time: %f\n" % (ct / retime))
    f.write("Ciphertext Num: %f\n" % (cn / retime))
    f.write("Plaintext Num: %f\n\n" % (pn / retime))

def exp1_func3(size):
    f.write("Experiment1 for 2^%d bytes file:\n" % size)
    exp1_func2(size, 32, 0.5, 40)



def exp1():
    f.write("Experiment1:\n")
    exp1_func3(10)
    exp1_func3(15)
    exp1_func3(20)
    exp1_func3(25)
    #exp1_func3(30)
    f.write("\n\n")

"""
Upload 10 files of size 2^20 bytes 400 times for each one
count the servertime, clienttime, 
"""
def exp2_func1(size, order, s, p, t, pt):
    fresh()
    server.setParameter(s, p, t, pt)
    client.setParameter(s, p, t)
    db = server.DataBase()
    clienttime = 0
    servertime = 0
    for i in range(400):
        filename = 'ExperimentFiles/file_%d_%d' % (size, order)
        t0 = time.time()
        up = client.OnceUpload(filename)
        xx = up.GetUploadFile()
        t1 = time.time()
        db.add(xx)
        t2 = time.time()
        clienttime += t1 - t0
        servertime += t2 - t1
    
    ciphernum = len(os.listdir("Ciphertexts"))
    plainnum = len(os.listdir("Plaintexts"))
    """f.write("Experiment 1 for 2^%d bytes:\n" % size)
    f.write("Server Time: %f\n" % servertime)
    f.write("Client Time: %f\n" % clienttime)
    f.write("Ciphertext Num: %d\n" % ciphernum)
    f.write("Plaintext Num: %d\n\n" % plainnum)"""
    print(plainnum)
    if plainnum == 0:
        sys.exit()
    return (servertime, clienttime, ciphernum, plainnum)

def exp2_func2(size, s, p, t, pt):
    st, ct, cn, pn = 0, 0, 0, 0
    for k in range (retime):
        for i in range(10):
            x = exp2_func1(size, i, s, p, t, pt)
            st += x[0]
            ct += x[1]
            cn += x[2]
            pn += x[3]
    f.write("Average with sigma = %d, p = %f, threshold = %d, picktime = %d:\n" % (s, p, t, pt))
    f.write("Server Time: %f\n" % (st / retime))
    f.write("Client Time: %f\n" % (ct / retime))
    f.write("Ciphertext Num: %f\n" % (cn / retime))
    f.write("Plaintext Num: %f\n\n" % (pn / retime))

def exp2_func3(size):
    exp2_func2(size, 32, 0.1, 10, 10)
    exp2_func2(size, 32, 0.5, 10, 10)
    exp2_func2(size, 32, 0.9, 10, 10)
    exp2_func2(size, 32, 0.1, 20, 10)
    exp2_func2(size, 32, 0.5, 20, 10)
    exp2_func2(size, 32, 0.9, 20, 10)
    exp2_func2(size, 200, 0.1, 10, 10)
    exp2_func2(size, 200, 0.5, 10, 10)
    exp2_func2(size, 200, 0.9, 10, 10)
    exp2_func2(size, 200, 0.1, 20, 10)
    exp2_func2(size, 200, 0.5, 20, 10)
    exp2_func2(size, 200, 0.9, 20, 10)
    exp2_func2(size, 32, 0.1, 10, 20)
    exp2_func2(size, 32, 0.5, 10, 20)
    exp2_func2(size, 32, 0.9, 10, 20)
    exp2_func2(size, 32, 0.1, 20, 20)
    exp2_func2(size, 32, 0.5, 20, 20)
    exp2_func2(size, 32, 0.9, 20, 20)
    exp2_func2(size, 200, 0.1, 10, 20)
    exp2_func2(size, 200, 0.5, 10, 20)
    exp2_func2(size, 200, 0.9, 10, 20)
    exp2_func2(size, 200, 0.1, 20, 20)
    exp2_func2(size, 200, 0.5, 20, 20)
    exp2_func2(size, 200, 0.9, 20, 20)

def exp2():
    f.write("Experiment2:\n")
    exp2_func3(20)

#exp1()
exp2()

