from socket import *
from threading import *

class ABReceiver:
    closingMessage = 'close'

    def __init__(self, delivery_buffer, recv_port):
        self._delivery_buffer = delivery_buffer
        self._is_receiving = False
        self._seq_num = '0'
        self._recv_port = recv_port
        

    def receive(self):
        my_socket = socket(AF_INET, SOCK_DGRAM) # create a socket
        my_socket.bind(('', self._recv_port))
        self._is_receiving = True
        while self.is_receiving():
            recv, destination_address = my_socket.recvfrom(4096) # receive data from the receieve portv
            source_port, destination_port, length, rcv_seq_num, is_ACK, checksum, data = self.parse(recv)
            print('Received packet:\n')
            self.print_packet(recv.decode())
            
            if self._seq_num == '0':
                if self.is_corrupt(recv, checksum) or (rcv_seq_num == '1'):
                    send_packet = self.make_pkt(self._recv_port, source_port, '1', '1', '')
                    my_socket.sendto(send_packet.encode(), destination_address)
                    print('Sending packet:\n')
                    self.print_packet(send_packet)
                elif rcv_seq_num == '0':
                    data = [destination_address, data]
                    self._delivery_buffer.put(data)
                    send_packet = self.make_pkt(self._recv_port, source_port, '0', '1', '')
                    my_socket.sendto(send_packet.encode(), destination_address)
                    print('Sending packet:\n')
                    self.print_packet(send_packet)
                    self._seq_num = '1'
                else:
                    print('An error has occured: self._seq_num = 0; no states activated')
            elif self._seq_num == '1':
                if self.is_corrupt(recv, checksum) or (rcv_seq_num == '0'):
                    send_packet = self.make_pkt(self._recv_port, source_port, '0', '1', '')
                    my_socket.sendto(send_packet.encode(), destination_address)
                    print('Sending packet:\n')
                    self.print_packet(send_packet)
                elif rcv_seq_num == '1':
                    data = [destination_address, data]
                    self._delivery_buffer.put(data)
                    send_packet = self.make_pkt(self._recv_port, source_port, '1', '1', '')
                    my_socket.sendto(send_packet.encode(), destination_address)
                    print('Sending packet:\n')
                    self.print_packet(send_packet)
                    self._seq_num = '0'
                else:
                    print('An error has occured: self._seq_num = 1; no states activated')        
            else:
                print('An error has occured: self._seq_num is neither 0 or 1')

    def terminate(self):
        self._is_receiving = False
        
    def is_receiving(self):
        return self._is_receiving

    def make_pkt(self, source_port, destination_port, seq_num, is_ACK, data):
        packet = ''
                                  
        sp = bin(source_port)[2:]
        while len(sp) < 16:
            sp = '0' + sp
        packet += sp

        dp = bin(destination_port)[2:]
        while len(dp) < 16:
            dp = '0' + dp
        packet += dp

        # length = header bits
        length = 96 + (len(data))
        l = bin(length)[2:]
        while len(l) < 16:
            l = '0' + l
        packet += l

        if seq_num == '0':
            packet += '00000000'
        elif seq_num == '1':
            packet += '11111111'
        else:
            packet += 'SEQERROR'
            print('An error has occured: no seq_num applied to made packet.\n data: ' + data)

        if is_ACK == '0':
            packet += '00000000'
        elif is_ACK == '1':
            packet += '11111111'
        else:
            packet += 'ACKERROR'
            print('An error has occured: no is_ACK applied to made packet.\n data: ' + data)

        packet += self.gen_checksum(packet)
        packet += data
        return packet
                        
    def gen_checksum(self, packet):
        sum_s = self.bin_add(packet[0:16], packet[16:32], packet[32:48], packet[48:56], packet[56:64])
        while len(sum_s) < 32:
            sum_s = '0' + sum_s
        sum_s = self.complement(sum_s)
        return sum_s
                             
    def is_corrupt(self, rcvpkt, checksum):
        rcvpkt = rcvpkt.decode()
        sum_s = self.gen_checksum(rcvpkt)
        if sum_s == checksum:
            return False
        else:
            return True

    def parse(self, recv):
        recv = recv.decode()
        source_port = int(recv[0:16], 2)
        destination_port = int(recv[16:32], 2)
        length = int(recv[32:48], 2)
        if recv[48:56] == '00000000':
            seq_num = '0'
        elif recv[48:56] == '11111111':
            seq_num = '1'
        else:
            seq_num = 'ERROR'
        if recv[56:64] == '00000000':
            ACK = '0'
        elif recv[56:64] == '11111111':
            ACK = '1'
        else:
            ACK = 'ERROR'
        checksum = recv[64:96]
        data = recv[96:]
        return source_port, destination_port, length, seq_num, ACK, checksum, data

    # source for this function: https://stackoverflow.com/questions/21420447/need-help-in-adding-binary-numbers-in-python
    def bin_add(self, *args):
        sum_s = 0
        for x in args:
            sum_s += int(x.encode(), 2)
        return bin(sum_s)[2:]

    def complement(self, bin_str):
        ret_str = ''
        for x in range(len(bin_str)):
            if bin_str[x] == '0':
                ret_str += '1'
            elif bin_str[x] == '1':
                ret_str += '0'
            else:
                ret_str += 'E'
        return ret_str
    
    def print_packet(self, packet):
        p = '+================+=================+\n'
        p += '|' + str(packet[0:16]) + '|' + str(packet[16:32]) + ' |\n'
        p += '+================+========+========+\n'
        p += '|' + str(packet[32:48]) + '|' + str(packet[48:56]) + '|' + str(packet[56:64]) + '|\n'
        p += '+================+========+========+\n'
        p += '|' + str(packet[64:96]) + '  |\n'
        p += '+==================================+\n'
        i = 0
        j = int(len(packet[96:]) / 32) + 1
        k = 96
        while i < j:
            if (k + 32) < len(packet):
                p += '|' + packet[k:k+32] + '  |\n'
                k += 32
            else:
                p += '|' + packet[k:] + ((32 - len(packet[k:])) * ' ') +  '  |\n'
            i += 1
        p += '+==================================+\n\n'
        print(p)

class ABSender:
    closingMessage = 'close'
    
    def __init__(self, destination_address, destination_port, recv_port):
        self._destination_address = destination_address
        self._seq_num = '0'
        self._destination_port = destination_port
        self._recv_port = recv_port
        self._timer = Timer(1.0, print("initialized"))
        self._timeout_status = False

    def send(self, data):
        my_socket = socket(AF_INET, SOCK_DGRAM) # create a socket
        my_socket.bind(('', self._recv_port))
        bytes_to_send = len(data)
        packet_length_limit = 4096 - 96           #altered from documentation for simplicity
        packets_to_send = int(bytes_to_send/(packet_length_limit)) + 1     #the 96 is the header length
        print(packets_to_send)
        i = 0
        x = 0
        packet_sent = False
        y = 1
        while i < packets_to_send: #while there are more packets to send
            print('Loop: ', y)
            y += 1
            print('i-value: ', i)
            if packet_sent == False:    #if this is the first packet to send
                print("packet_sent == False")
                if x + packet_length_limit < len(data):     #if there are multiple packets to send
                    send_data = data[x:x+packet_length_limit]
                    x += packet_length_limit
                else:
                    send_data = data[x:]    #if there is one packet to send
                    x += packet_length_limit
                send_packet = self.make_pkt(self._recv_port, self._destination_port, self._seq_num, '0', send_data) #send the packet
                print('Sending packet:\n')
                self.print_packet(send_packet)
                packet_sent = True
                self._timer = Timer(4.0, self.time_out, [my_socket, x, data, packet_length_limit])
                self._timer.start()
                my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
            else:
                recv, d_a = my_socket.recvfrom(4096)
                s_p, d_p, length, rcv_seq_num, is_ACK, checksum, recv_data = self.parse(recv)
                print('Received packet:\n')
                self.print_packet(recv.decode())
        
                print("else")
                if self.is_corrupt(recv, checksum) == False and is_ACK == '1' and i == packets_to_send - 1: #if we receieve an ACK and this is the last packet to send
                    if rcv_seq_num == self._seq_num:    #if the ACK matches the seq
                        self._timer.cancel()
                        self._timeout_status = False
                        if self._seq_num == '0':        #adjust the seq number
                            self._seq_num = '1'
                        else:
                            self._seq_num = '0'
                        x += packet_length_limit        #increment our counters, the loop will not trigger again
                        i += 1                          #this is because now, i == packets_to_send
                    else:   #if the ACK doesn't match the seq
                        self._timer.cancel()
                        self._timeout_status = False
                        send_data = data[x - packet_length_limit:]  #resend the previous data
                        send_packet = self.make_pkt(self._recv_port, self._destination_port, self._seq_num, '0', send_data)
                        print('Sending packet:\n')
                        self.print_packet(send_packet)
                        my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
                        self._timer = Timer(4.0, self.time_out, [my_socket, x, data, packet_length_limit])
                        self._timer.start()
                elif self.is_corrupt(recv, checksum) == False and is_ACK == '1':    #if we receieve an ACK and this is not the last packet to send
                    if rcv_seq_num == self._seq_num:    #if the ACK matches the seq
                        self._timer.cancel()
                        self._timeout_status = False
                        if self._seq_num == '0':        #adjust the seq number
                            self._seq_num = '1'
                        else:
                            self._seq_num = '0'
                        if x + packet_length_limit < len(data):         #if this isn't the last packet
                            send_data = data[x:x+packet_length_limit]   #send the next packet_length_limit of data
                            x += packet_length_limit                    #and adjust the counter
                        else:                                           #if it's not the last packet (this should not occur)
                            send_data = data[x:]                        #send the last segment of data
                        send_packet = self.make_pkt(self._recv_port, self._destination_port, self._seq_num, '0', send_data)
                        print('Sending packet:\n')
                        self.print_packet(send_packet)
                        self._timer = Timer(4.0, self.time_out, [my_socket, x, data, packet_length_limit])
                        self._timer.start()
                        i += 1
                        my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
                    else:       #if we receive an ACK and it does not match the seq
                        self._timer.cancel()    #restart the timer
                        self._timeout_status = False
                        if x < len(data):
                            send_data = data[x-packet_length_limit:x]   #back up and send the last data segment
                            #x += packet_length_limit
                        else:
                            send_data = data[x-packet_length_limit:]    #if x is beyond the bounds of data to send, send the last data segment up to the end
                        send_packet = self.make_pkt(self._recv_port, self._destination_port, self._seq_num, '0', send_data)
                        print('Sending packet:\n')
                        self.print_packet(send_packet)
                        my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
                        self._timer = Timer(4.0, self.time_out, [my_socket, x, data, packet_length_limit])
                        self._timer.start()
        print("Sending has completed.")
        #my_socket.shutdown(SHUT_RDWR)
        my_socket.close()
                       
    def time_out(self, my_socket, x, data, packet_length_limit):
        self._timeout_status = True
        print("Timed out!")
        if x < len(data):
            send_data = data[x-packet_length_limit:x]
        else:
            send_data = data[x-packet_length_limit:]
        send_packet = self.make_pkt(self._recv_port, self._destination_port, self._seq_num, '0', send_data)
        print('Sending packet:\n')
        self.print_packet(send_packet)
        self._timer.cancel()
        self._timer = Timer(4.0, self.time_out, [my_socket, x, data, packet_length_limit])
        self._timer.start()
        my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
        
    def terminate():
        self._is_receiving = False
        
    def is_receiving():
        return self._is_receiving

    def make_pkt(self, source_port, destination_port, seq_num, is_ACK, data):
        packet = ''
                                  
        sp = bin(source_port)[2:]
        while len(sp) < 16:
            sp = '0' + sp
        packet += sp

        dp = bin(destination_port)[2:]
        while len(dp) < 16:
            dp = '0' + dp
        packet += dp

        # length = header bits 
        length = 96 + (len(data))
        l = bin(length)[2:]
        while len(l) < 16:
            l = '0' + l
        packet += l

        if seq_num == '0':
            packet += '00000000'
        elif seq_num == '1':
            packet += '11111111'
        else:
            packet += 'SEQERROR'
            print('An error has occured: no seq_num applied to made packet.\n data: ' + data)

        if is_ACK == '0':
            packet += '00000000'
        elif is_ACK == '1':
            packet += '11111111'
        else:
            packet += 'ACKERROR'
            print('An error has occured: no is_ACK applied to made packet.\n data: ' + data)

        packet += self.gen_checksum(packet)
        packet += data
        return packet
                        
    def gen_checksum(self, packet):
        sum_s = self.bin_add(packet[0:16], packet[16:32], packet[32:48], packet[48:56], packet[56:64])
        while len(sum_s) < 32:
            sum_s = '0' + sum_s
        sum_s = self.complement(sum_s)
        return sum_s
                             
    def is_corrupt(self, rcvpkt, checksum):
        rcvpkt = rcvpkt.decode()
        sum_s = self.gen_checksum(rcvpkt)
        if sum_s == checksum:
            return False
        else:
            return True
        
    def parse(self, recv):
        recv = recv.decode()
        source_port = int(recv[0:16], 2)
        destination_port = int(recv[16:32], 2)
        length = int(recv[32:48], 2)
        if recv[48:56] == '00000000':
            seq_num = '0'
        elif recv[48:56] == '11111111':
            seq_num = '1'
        else:
            seq_num = 'ERROR'
        if recv[56:64] == '00000000':
            ACK = '0'
        elif recv[56:64] == '11111111':
            ACK = '1'
        else:
            ACK = 'ERROR'
        checksum = recv[64:96]
        data = recv[96:]
        return source_port, destination_port, length, seq_num, ACK, checksum, data

    # source for this function: https://stackoverflow.com/questions/21420447/need-help-in-adding-binary-numbers-in-python
    def bin_add(self, *args):
        sum_s = 0
        for x in args:
            sum_s += int(x.encode(), 2)
        return bin(sum_s)[2:]

    def complement(self, bin_str):
        ret_str = ''
        for x in range(len(bin_str)):
            if bin_str[x] == '0':
                ret_str += '1'
            elif bin_str[x] == '1':
                ret_str += '0'
            else:
                ret_str += 'E'
        return ret_str

    def print_packet(self, packet):
        p = '+================+=================+\n'
        p += '|' + str(packet[0:16]) + '|' + str(packet[16:32]) + ' |\n'
        p += '+================+========+========+\n'
        p += '|' + str(packet[32:48]) + '|' + str(packet[48:56]) + '|' + str(packet[56:64]) + '|\n'
        p += '+================+========+========+\n'
        p += '|' + str(packet[64:96]) + '  |\n'
        p += '+==================================+\n'
        i = 0
        j = int(len(packet[96:]) / 32) + 1
        k = 96
        while i < j:
            if (k + 32) < len(packet):
                p += '|' + packet[k:k+32] + '  |\n'
                k += 32
            else:
                p += '|' + packet[k:] + ((32 - len(packet[k:])) * ' ') +  '  |\n'
            i += 1
        p += '+==================================+\n\n'
        print(p)
