from socket import *
from ABProtocol import *
import threading

class begin_receive_thread(threading.Thread):
    def __init__(self, receiver):
        threading.Thread.__init__(self)
        self._receiver = receiver
    def run(self):
        print("starting receiver")
        self._receiver.receive()
        #print("starting receiver22")

def main():
    #client port = 50001
    data = "THIS IS A TEST STRING. THIS STRING IS TESTING NOW. RATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRATRAT"
    sender = ABSender('localhost', 12020, 50001)
    sender.send(data)
    
if __name__ == '__main__':
    main()
