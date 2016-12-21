import time


class Timer():
    def __init__(self, print=True):
        self.start_time = None
    def __enter__(self):
        self.start_time = time.time()
    def __exit__(self, itype, value, traceback):
        self.end_time = time.time()
        diff = self.end_time - self.start_time
        print('time taken: {0:.6f} seconds'.format(diff))
