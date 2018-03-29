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
        #print("starting receiver22")

def main():
    #server port = 12020
    buffer = Queue()
    buffer.daemon = True
    data = ''
    receiver = ABReceiver(buffer, 12020)
    t1 = begin_receive_thread(receiver)
    t1.start()
    while 1:
        if not buffer.empty():
            recv = buffer.get()
            data += recv[1]
            print ("addr: ", recv[0][0], " | port: ", recv[0][1], " | data: ", data)
        else:
            time.sleep(3)

if __name__ == '__main__':
   main()
