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

def ab_protocol(server_address, server_port, client_rcv_port, client_send_port, file_name):
    sender = ABSender(server_address, server_port, client_send_port)
    buffer = Queue()
    buffer.daemon = True
    data = ''
    receiver = ABReceiver(buffer, client_rcv_port)
    t1 = begin_receive_thread(receiver)
    t1.start()
    sender.send(str(file_name + '@@@' + str(client_rcv_port)))
    sender.send('SEND COMPLETE')
    while receiver.is_receiving():
        if not buffer.empty():
            recv = buffer.get()
            if recv[1] == 'SEND COMPLETE':
                time.sleep(3)
                receiver.terminate()
                #print(data)
                f = open(file_name, 'wb')
                f.write(data.encode())
            elif recv[1] != '':
                data += recv[1]
            else:
                time.sleep(0.5)
            
def main():
    #client port = client_port
    server_address = input("Please enter EXACTLY the server address. For local machine testing, enter 'localhost' with no apostrophes. [Note: there is no error checking here, so enter it correctly.]\n")

    server_port = -1
    while not (1024 <= server_port and server_port <= 65535):
        server_port = int(input("Please enter the receive port for the server. [Note: port must be an integer 1024-65535]\n"))

    client_rcv_port = -1
    while not (1024 <= client_rcv_port and client_rcv_port <= 65535):
        client_rcv_port = int(input("Please enter the port for this client's receiver. [Note: port must be an integer 1024-65535]\n"))

    client_send_port = -1
    while not (1024 <= client_send_port and client_send_port <= 65535):
        client_send_port = int(input("Please enter the port for this client's sender. [Note: port must be an integer 1024-65535], and must be different from the receiver. This port is used for sending data from the client to the server].\n"))

    file_name = input("Please enter EXACTLY the filename of the text file. [Note: there is no error checking here, so enter it correctly.]\n")

    protocol = -1
    while not (protocol == 1 or protocol == 2):
        protocol = int(input("Please enter 1 to use ABProtocol or 2 to use SRProtocol. [Note: the program must be restarted to use a different protocol.\n"))

    if protocol == 1:
        ab_protocol(server_address, server_port, client_rcv_port, client_send_port, file_name)
    else:
        time.sleep(1)    
    
if __name__ == '__main__':
    main()
