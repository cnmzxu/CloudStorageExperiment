import os

def genFile(length):
    for i in range(10):
        f = open("ExperimentFiles/file_%d_" % length + str(i), 'wb')
        f.write(os.urandom(2 ** length))
        f.close()

try:
    os.mkdir("ExperimentFiles")
except:
    None
genFile(10)
genFile(15)
genFile(20)
genFile(25)
#genFile(30)
