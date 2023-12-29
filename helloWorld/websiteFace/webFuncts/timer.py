import time


class Timer:
    def __init__(self):
        self.start_time = time.time()

    def get_start_time(self):
        return self.start_time

    def end_time(self):
        return time.time() - self.start_time
