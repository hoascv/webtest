from threading import Thread
import threading
import time
import logging
from random import randint

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


class Vsu(Thread):

    def __init__(self, target=None, name=None, args=(), kwargs=None):
        super().__init__(name=name, target=target)
        self.args = args
        self.kwargs = kwargs
        self.request_id = 0

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        return






class DATS(Thread):

    def __init__(self, target=None, name=None, args=(), kwargs=None):
        super().__init__(name=name, target=target, )
        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        return

def test():
    logging.debug('Starting ...')
    print(threading.current_thread().name)


    time.sleep(randint(0, 10))
    logging.debug('Exiting ...')



def main():
    for i in range(5):
        t = Vsu(name='vsu' + str(i).zfill(4), args=(i,),target=test, kwargs={'nome': 'helder', 'apelido': 'Sousa'})
        t.start()

    t.join()




if __name__ == '__main__':
    main()
