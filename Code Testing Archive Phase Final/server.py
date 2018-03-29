from socket import *
from ABProtocol import *
from SRProtocol import *
import threading
from queue import *
from itertools import chain
import time

class begin_receive_thread(threading.Thread):
    def __init__(self, receiver):
        threading.Thread.__init__(self)
        self._receiver = receiver
    def run(self):
        print("starting receiver")
        self._receiver.receive()
        #print("starting receiver22")

def ab_protocol(server_rcv_port, server_send_port, file_path):
    connections = []
    buffer = Queue()
    buffer.daemon = True
    data = ''
    receiver = ABReceiver(buffer, server_rcv_port)
    t1 = begin_receive_thread(receiver)
    t1.start()
    while 1:
        #print('1')
        if not buffer.empty():
            recv = buffer.get()
            client_address = recv[0][0]
            client_send_port = recv[0][1]
            print("Bufferdata: " + str(client_address) + " " + str(client_send_port) + " " + recv[1])
            
            if not (recv[1] == '' or recv[1] == 'SEND COMPLETE'):
                print('here 1')
                if not [client_address, client_send_port] in chain(*connections):
                    print('here 2')
                    connections.append([client_address, client_send_port])
                    recv_split = recv[1].split('@@@')
                    file_name = recv_split[0]
                    if '\\' in file_path:
                        adj_file_name = file_path + '\\' + file_name
                    else:
                        adj_file_name = file_path + '/' + file_name
                    try:
                        print (adj_file_name)
                        with open(adj_file_name, 'rb') as f:
                            data = f.read().decode()
                    except IOError:
                        data = 'ERROR: File does not exist'
                        print('File path: ' + adj_file_name)
                        print(data)
                        
                    client_rcv_port = int(recv_split[1])
                    sender = ABSender(client_address, client_rcv_port, server_send_port)
                    start_time = time.time()
                    sender.send(data)
                    sender.send('SEND COMPLETE')
                    end_time = time.time()
                    print(connections)
                    for x in connections[:]:
                        if x[1] == client_send_port:
                            connections.remove(x)
                    print(connections)
                    time_to_send = end_time - start_time
                    print("Sending took ", time_to_send, " seconds!")
                    print ("addr: ", client_address, " | port: ", client_rcv_port, " | data: ", data[:20])
        else:
            time.sleep(1)

def sr_protocol(server_rcv_port, server_send_port, file_path, window_size):
    connections = []
    buffer = Queue()
    buffer.daemon = True
    data = ''
    receiver = SRReceiver(buffer, server_rcv_port, window_size)
    t1 = begin_receive_thread(receiver)
    t1.start()
    while 1:
        #print('1')
        if not buffer.empty():
            recv = buffer.get()
            client_address = recv[0][0]
            client_send_port = recv[0][1]
            print("Bufferdata: " + str(client_address) + " " + str(client_send_port) + " " + recv[1])
            
            if not (recv[1] == '' or recv[1] == 'SEND COMPLETE'):
                print('here 1')
                if not [client_address, client_send_port] in chain(*connections):
                    print('here 2')
                    connections.append([client_address, client_send_port])
                    recv_split = recv[1].split('@@@')
                    file_name = recv_split[0]
                    if '\\' in file_path:
                        adj_file_name = file_path + '\\' + file_name
                    else:
                        adj_file_name = file_path + '/' + file_name
                    try:
                        print (adj_file_name)
                        with open(adj_file_name, 'rb') as f:
                            data = f.read().decode()
                    except IOError:
                        data = 'ERROR: File does not exist'
                        print('File path: ' + adj_file_name)
                        print(data)
                        
                    client_rcv_port = int(recv_split[1])
                    sender = SRSender(client_address, client_rcv_port, server_send_port, window_size)
                    start_time = time.time()
                    sender.send(data)
                    sender.send('SEND COMPLETE')
                    end_time = time.time()
                    print(connections)
                    for x in connections[:]:
                        if x[1] == client_send_port:
                            connections.remove(x)
                    print(connections)
                    time_to_send = end_time - start_time
                    print("Sending took ", time_to_send, " seconds!")
                    print ("addr: ", client_address, " | port: ", client_rcv_port, " | data: ", data[:20])
        else:
            time.sleep(1)

def main():
    server_rcv_port = -1
    while not (1024 <= server_rcv_port and server_rcv_port <= 65535):
        server_rcv_port = int(input("Please enter the port for this server's receiver. [Note: port must be an integer 1024-65535]\n"))

    server_send_port = -1
    while not (1024 <= server_send_port and server_send_port <= 65535):
        server_send_port = int(input("Please enter the port for this server's sender. [Note: port must be an integer 1024-65535], and must be different from the receiver. This port is used for sending data from the server to the client.]\n"))

    file_path = input("Please enter EXACTLY the filepath of the text file. [Note: there is no error checking here, so enter it correctly.]\n")
    
    protocol = -1
    while not (protocol == 1 or protocol == 2):
        protocol = int(input("Please enter 1 to use ABProtocol or 2 to use SRProtocol. [Note: the program must be restarted to use a different protocol.\n"))

    if protocol == 1:
        ab_protocol(server_rcv_port, server_send_port, file_path)
    else:
        sr_protocol(server_rcv_port, server_send_port, file_path, 10)    

if __name__ == '__main__':
    main()
