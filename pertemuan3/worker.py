import threading
import logging

class MyThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        logging.debug(str(self.num) + ' running')

for i in range(5):
    t = MyThread(i)
    t.start()