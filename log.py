class Log:
    def __init__(self, logfile1 = 'clog.txt', logfile2 = 'slog.txt'):
        self.f1 = open(logfile1, 'a')
        self.f2 = open(logfile2, 'a')

    def __del__(self):
        self.f1.close()
        self.f2.close()

    def clientlog(self, upfile, flag, cipher, hv, lag, key, randbytes):
        self.f1.write("%s -> %s, flag is %d:\n" % (upfile, cipher, flag))
        self.f1.write("hash value: %s\n" % str(hv))
        self.f1.write("lag: %d\n" % lag)
        self.f1.write("key: %s\n" % str(key))
        self.f1.write("randbytes: %d\n" % randbytes)
        self.f1.write("\n")


    def serverlog(self, logtext):
        self.f2.write(logtext)

