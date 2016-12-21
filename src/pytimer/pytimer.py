import time


class Timer():
    def __init__(self, print=True, title=None):
        self.start_time = None
        self.title = title
    def __enter__(self):
        self.start_time = time.time()
    def __exit__(self, itype, value, traceback):
        self.end_time = time.time()
        diff = self.end_time - self.start_time
        if self.print:
            if title:
                print('time taken for {title}: {0:.6fdiff} seconds'.format(title=self.title, diff=diff))
            else:
                print('time taken: {0:.6fdiff} seconds'.format(diff=diff))
