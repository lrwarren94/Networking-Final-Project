from socket import *
from ABProtocol import *
import threading
from queue import *
import time

class begin_receive_thread(threading.Thread):
    def __init__(self, receiver):
        threading.Thread.__init__(self)
        self._receiver = receiver
    def run(self):
        print("starting receiver")
        self._receiver.receive()
        print("starting receiver22")
    #def get_buffer(self):
        #return self._receiver.get_buffer()

def main():
    #server port = 12020
    buffer = Queue()
    buffer.daemon = True
    data = ''
    receiver = ABReceiver(buffer, 12020)
    t1 = begin_receive_thread(receiver)
    #target=begin_receive, args=(receiver,))
    t1.start()
    while 1:#print('here 11111111111111111')
        #buffer = t1.get_buffer()
        if not buffer.empty():
            data += buffer.get()
            print (data)
        else:
            time.sleep(3)

if __name__ == '__main__':
   main()
