import client
import sssa
import random
import translation
import server
import time

#test1: check out if enc and dec in client.py is matchable 
def test1(filename):
    upload = client.OnceUpload(filename)
    key = upload.GetKeys()
    ciphername = upload.GetUploadFile()[2]
    print(client.DecryptFile(key[0], key[1], ciphername))

#test2: check out if secret sharing is right
def test2():
    a = [random.randint(0, 255) for i in range(64)]
    print(a)
    ss = sssa.sssa(30, 70)
    shares = [ss.share([221] + a + [255] * 5) for i in range(30)]
    print(ss.recovery(shares))

def test3():
    clienttime = 0
    servertime = 0
    db = server.DataBase()
    for i in range(1):
        filename = 'ExperimentFiles/file_10_' + str(i)
        for k in range(40):
            t0 = time.time()
            up = client.OnceUpload(filename)
            t1 = time.time()
            db.add(up.GetUploadFile())
            t2 = time.time()
            clienttime += t1 - t0
            servertime += t2 - t1

    print("Server Time: %d" % servertime)
    print("Client Time: %d" % clienttime)

def test4():
    try:
        os.remove('asdfasdfadsfasdfadsfasf')
    except:
        print()
test2()
