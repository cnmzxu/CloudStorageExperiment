class myerror(Exception):
    def __init__(self, message):
        self.message = message
        print(message)
        Exception.__init__(self, message)