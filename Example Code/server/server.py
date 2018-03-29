from socket import *
import os
import math

def parse(recv):
        filename = recv[0:-1].decode() #get the file name
        ACK = recv[-1:] #get ACK number
        return filename, int(ACK)


def main():
        serverPort = 12020
        closingMessage = 'close'
        serverSocket = socket(AF_INET, SOCK_DGRAM)#create a socket
        serverSocket.bind(('', serverPort))     
        seqnumber = 0
        m_ACK = 0
        recv_Str = ''
        i = 0
        file_recv = 'OK'
        print('The server is ready to receive:')
        while 1:                        
                recv, clientAddress = serverSocket.recvfrom(1024) #receive data from client
                print(recv.decode(), clientAddress)             
                recv_Str,ACK = parse(recv)
                print('recv_Str:',recv_Str)
                print('ACK:',ACK)
                if recv_Str != '':
                        if recv_Str == 'close':
                                print('file is sent completely!')
                                f.close()
                        else:

                                f_size = os.stat(recv_Str).st_size #get the file size
                                try:
                                        f = open(recv_Str, 'rb')
                                        serverSocket.sendto(str.encode(file_recv)+bytes([ACK]),clientAddress)
                                        number_data = math.ceil(f_size/1024)  # get the data numeber we need to send to the client
                                        if m_ACK == ACK:
                                                m_ACK = (m_ACK+1)%2
                                                print("I am here")
                                except IOError:
                                        print("file open error!")                                                       
                else:
                        print("m_ACK:", m_ACK)
                        if m_ACK == ACK:
                                i = i+1
                        else:
                                f.seek(-1024,1)
                        resp_data = f.read(1024)                

                        if i == number_data:
                                serverSocket.sendto(str.encode(closingMessage)+bytes([ACK]),clientAddress)
                        else:
                                serverSocket.sendto(resp_data+bytes([ACK]),clientAddress)
                

if __name__ == '__main__':

        main()
