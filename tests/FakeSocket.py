import errno
import os

class FakeSocket:
    @staticmethod
    def socket():
        return FailingConnection()
        
# not sure how this works so cannot mock correctly yet
    def error(self):
        return os.strerror(errno.ENOENT)

class FailingConnection:
    def __init__(self):
        pass

    def connect(self, args):
        raise IOError("Something went wrong bad connection")

    def close(self):
        pass