from socket import *
from threading import *

class SRReceiver:
    closingMessage = 'close'

    def __init__(self, delivery_buffer, recv_port, window_size):
        self._delivery_buffer = delivery_buffer
        self._window_size = window_size
        self._seq_buffer_size = 100
        self._seq_buffer = ['INIT'] * self._seq_buffer_size   #this is the data buffer
        self._send_base = 0
        self._is_receiving = False
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

            if not self.is_corrupt(recv, checksum):
                if (rcv_seq_num >= self._send_base and (rcv_seq_num <= (self._send_base + self._window_size - 1))) or ((self._seq_buffer_size - 1 < self._send_base + self._window_size - 1) and (rcv_seq_num <= (self._send_base + self._window_size - 1) % self._seq_buffer_size)):
                    if self._seq_buffer[rcv_seq_num] == 'INIT':
                        self._seq_buffer[rcv_seq_num] = data
                        send_packet = self.make_pkt(self._recv_port, source_port, rcv_seq_num, '1', '')
                        my_socket.sendto(send_packet.encode(), destination_address)
                        print('Sending packet:\n')
                        if rcv_seq_num == self._send_base:
                            consecutive = True
                            while consecutive:
                                if self._seq_buffer[self._send_base] != 'INIT':
                                    self._delivery_buffer.put([destination_address, self._seq_buffer[self._send_base]])
                                    self._seq_buffer[self._send_base] = 'INIT'
                                    if self._send_base == self._seq_buffer_size - 1:
                                        self._send_base = 0
                                    else:
                                        self._send_base += 1
                                else:
                                    consecutive = False
                    else:
                        send_packet = self.make_pkt(self._recv_port, source_port, rcv_seq_num, '1', '')
                        my_socket.sendto(send_packet.encode(), destination_address)
                        print('Sending packet:\n')
                elif rcv_seq_num >= ((self._send_base - self._window_size + self._seq_buffer_size) % self._seq_buffer_size) and rcv_seq_num <= ((self._send_base - 1 + self._seq_buffer_size) % self._seq_buffer_size):
                        send_packet = self.make_pkt(self._recv_port, source_port, rcv_seq_num, '1', '')
                        my_socket.sendto(send_packet.encode(), destination_address)
                        print('Sending packet:\n')
                    

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

        packet += bin(seq_num)[2:].zfill(8)

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
        seq_num = int(recv[48:56], 2)
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

class SRSender:
    closingMessage = 'close'
    
    def __init__(self, destination_address, destination_port, recv_port, window_size):
        self._destination_address = destination_address
        self._window_size = window_size
        self._seq_buffer_size = 100
        self._seq_buffer = []   #this is the data buffer
        for i in range(0, self._seq_buffer_size):    
            self._seq_buffer.append(['INIT', 0])
        self._send_base = 0
        self._destination_port = destination_port
        self._recv_port = recv_port
        self._timer_list = []
        for i in range(0, self._seq_buffer_size):
            self._timer_list.append([Timer(5.0, self.dummy_method), 0])

    def send(self, data):
        my_socket = socket(AF_INET, SOCK_DGRAM) # create a socket
        my_socket.bind(('', self._recv_port))
        bytes_to_send = len(data)
        packet_length_limit = 4096 - 96           #altered from documentation for simplicity
        packets_to_send = int(bytes_to_send/(packet_length_limit)) + 1     #the 96 is the header length
        print(packets_to_send)
        sent_packets = 0    #number of packets successfully sent so far
        packet_sent = False
        y = 1   #counter used for bugtesting
        data_to_send = []
        dts_index = 0    #index that assists in adjusting what data needs to be sent to the seq buffer
        
        for i in range(0, packets_to_send): #set up an array containing the data for each packet to be sent
            if i + 1 == packets_to_send:
                data_to_send.append(data[i * 4000:])
            else:
                data_to_send.append(data[i * 4000:(i + 1)*4000])
        
        #if statement is new code 
        if (self._send_base + self._window_size - 1) % self._seq_buffer_size < self._send_base:
            limit = self._seq_buffer_size
            for i in range(self._send_base, limit): #set up the sequence buffer for the first time
                if dts_index < packets_to_send:
                    self._seq_buffer[i][0] = data_to_send[dts_index]
                    dts_index += 1
            for i in range(0, (self._send_base + self._window_size - 1) % self._seq_buffer_size): #set up the sequence buffer for the first time
                if dts_index < packets_to_send:
                    self._seq_buffer[i][0] = data_to_send[dts_index]
                    dts_index += 1    
        else:
            limit = self._send_base + self._window_size
            for i in range(self._send_base, limit): #set up the sequence buffer for the first time
                if dts_index < packets_to_send:
                    self._seq_buffer[i][0] = data_to_send[dts_index]
                    dts_index += 1
        #formerly: 0, self._window_size #formerly 2: 0, self._seq_buffer_size
        #for i in range(self._send_base, self._send_base + self._window_size): #set up the sequence buffer for the first time
        #    if not i > len(data_to_send) - 1:
        #        self._seq_buffer[i][0] = data_to_send[i]
        #        dts_index += 1

        #print(" seq_buffer " + str(self._seq_buffer) + "  dts  " + str(dts_index))
        #print(data_to_send)
        while sent_packets < packets_to_send: #while there are more packets to send
            print('Loop: ', y)
            y += 1
            if packet_sent == False:    #if this is the first packet to send
                print("packet_sent == False")
                packet_sent = True
                if (self._send_base + self._window_size - 1) % self._seq_buffer_size < self._send_base:
                    limit = self._seq_buffer_size
                    for i in range(self._send_base, limit):
                        if self._seq_buffer[i][0] != 'INIT':
                            send_packet = self.make_pkt(self._recv_port, self._destination_port, i, '0', self._seq_buffer[i][0]) #send the packet

                            print('Sending packet:\n')
                            print('send base: ' + str(self._send_base) + '\n')
                            print('window cap: ' + str(self._send_base + self._window_size - 1) + '\n')
                            print('dts_index: ' + str(dts_index) + '\n')
                            print('i-num: ' + str(i) + '\n')
                            print('buffer sample data: ' + self._seq_buffer[i][0][:10] + '\n')
                            ack_count = 0
                            for i in range (0, self._seq_buffer_size):
                                if self._seq_buffer[i][1] == 1:
                                    ack_count += 1
                            print('ACK snapshot: ' + str(ack_count) + '\n')
                            print('packets sent: ' + str(sent_packets) + '\n')

                            self.print_packet(send_packet)
                            self._timer_list[i][0] = Timer(5.0, self.time_out, args=(my_socket, i,))
                            self._timer_list[i][0].start()
                            my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
                    for i in range(0, (self._send_base + self._window_size - 1) % self._seq_buffer_size):
                        if self._seq_buffer[i][0] != 'INIT':
                            send_packet = self.make_pkt(self._recv_port, self._destination_port, i, '0', self._seq_buffer[i][0]) #send the packet

                            print('Sending packet:\n')
                            print('send base: ' + str(self._send_base) + '\n')
                            print('window cap: ' + str(self._send_base + self._window_size - 1) + '\n')
                            print('dts_index: ' + str(dts_index) + '\n')
                            print('i-num: ' + str(i) + '\n')
                            print('buffer sample data: ' + self._seq_buffer[i][0][:10] + '\n')
                            ack_count = 0
                            for i in range (0, self._seq_buffer_size):
                                if self._seq_buffer[i][1] == 1:
                                    ack_count += 1
                            print('ACK snapshot: ' + str(ack_count) + '\n')
                            print('packets sent: ' + str(sent_packets) + '\n')

                            self.print_packet(send_packet)
                            self._timer_list[i][0] = Timer(5.0, self.time_out, args=(my_socket, i,))
                            self._timer_list[i][0].start()
                            my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
                else:
                    for i in range (self._send_base, self._send_base + self._window_size):
                        if self._seq_buffer[i][0] != 'INIT':
                            send_packet = self.make_pkt(self._recv_port, self._destination_port, i, '0', self._seq_buffer[i][0]) #send the packet

                            print('Sending packet:\n')
                            print('send base: ' + str(self._send_base) + '\n')
                            print('window cap: ' + str(self._send_base + self._window_size - 1) + '\n')
                            print('dts_index: ' + str(dts_index) + '\n')
                            print('i-num: ' + str(i) + '\n')
                            print('buffer sample data: ' + self._seq_buffer[i][0][:10] + '\n')
                            ack_count = 0
                            for i in range (0, self._seq_buffer_size):
                                if self._seq_buffer[i][1] == 1:
                                    ack_count += 1
                            print('ACK snapshot: ' + str(ack_count) + '\n')
                            print('packets sent: ' + str(sent_packets) + '\n')

                            self.print_packet(send_packet)
                            self._timer_list[i][0] = Timer(5.0, self.time_out, args=(my_socket, i,))
                            self._timer_list[i][0].start()
                            my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
            else:
                recv, d_a = my_socket.recvfrom(4096)
                s_p, d_p, length, rcv_seq_num, is_ACK, checksum, recv_data = self.parse(recv)
                print('Received packet:\n')
                self.print_packet(recv.decode())
                print("else")
                       
                if not self.is_corrupt(recv, checksum):
                    #if the ACK is in the window
                    if (rcv_seq_num >= self._send_base and (rcv_seq_num <= (self._send_base + self._window_size - 1))) or ((self._seq_buffer_size - 1 < self._send_base + self._window_size - 1) and (rcv_seq_num <= (self._send_base + self._window_size - 1) % self._seq_buffer_size)):
                        self._seq_buffer[rcv_seq_num][1] = 1
                        self._timer_list[rcv_seq_num][0].cancel()
                        self._timer_list[rcv_seq_num][1] = 1
                        sent_packets += 1

                        if rcv_seq_num == self._send_base:
                            consecutive = True
                            while consecutive:
                                if self._seq_buffer[self._send_base][1] == 1:
                                    self._seq_buffer[self._send_base][0] = 'INIT'
                                    self._seq_buffer[self._send_base][1] = 0
                                    if self._send_base == self._seq_buffer_size - 1:
                                        self._send_base = 0
                                    else:
                                        self._send_base += 1
                                    if dts_index < packets_to_send:                                 #corrected
                                        seq_num = (self._send_base + self._window_size - 1) % self._seq_buffer_size
                                        self._seq_buffer[seq_num][0] = data_to_send[dts_index]
                                        self._seq_buffer[seq_num][1] = 0
                                        dts_index += 1
                                        send_packet = self.make_pkt(self._recv_port, self._destination_port, seq_num, '0', self._seq_buffer[seq_num][0])

                                        print('send base: ' + str(self._send_base) + '\n')
                                        print('window cap: ' + str(self._send_base + self._window_size - 1) + '\n')
                                        print('dts_index: ' + str(dts_index) + '\n')
                                        print('seq-num: ' + str(rcv_seq_num) + '\n')
                                        print('buffer sample data: ' + self._seq_buffer[rcv_seq_num][0][:10] + '\n')
                                        ack_count = 0
                                        for i in range (0, self._seq_buffer_size):
                                            if self._seq_buffer[i][1] == 1:
                                                ack_count += 1
                                        print('ACK snapshot: ' + str(ack_count) + '\n')
                                        print('packets sent: ' + str(sent_packets) + '\n')

                                        print('Sending packet:\n')
                                        self.print_packet(send_packet)
                                        my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))
                                        self._timer_list[seq_num][0] = Timer(5.0, self.time_out, args=(my_socket, seq_num,))
                                        self._timer_list[seq_num][1] = 0
                                else:
                                    consecutive = False
        print("Sending has completed.")
        my_socket.close()

        #reset the variables so send can be called again with the same object
        self._seq_buffer = []   #this is the data buffer
        for i in range(0, self._seq_buffer_size):    
            self._seq_buffer.append(['INIT', 0])
        #self._send_base = 0
        #self._timer_list = []
        #for i in range(0, self._seq_buffer_size):
         #   self._timer_list.append([Timer(5.0, self.dummy_method), 0])
        for i in range(0, self._seq_buffer_size):
            self._timer_list[i][0].cancel()
            self._timer_list[i] = [Timer(5.0, self.dummy_method), 1]


    def time_out(self, my_socket, seq_num,):
        if self._timer_list[seq_num][1] != 1:
            print("Timed out!\n")
            send_data = self._seq_buffer[seq_num][0]
            send_packet = self.make_pkt(self._recv_port, self._destination_port, seq_num, '0', send_data)

            print('send base: ' + str(self._send_base) + '\n')
            print('window cap: ' + str(self._send_base + self._window_size - 1) + '\n')
            print('seq-num: ' + str(seq_num) + '\n')
            print('buffer sample data: ' + self._seq_buffer[seq_num][0][:10] + '\n')
            ack_count = 0
            for i in range (0, self._seq_buffer_size):
                if self._seq_buffer[i][1] == 1:
                    ack_count += 1
            print('ACK snapshot: ' + str(ack_count) + '\n')

            print('Sending packet:\n')
            self.print_packet(send_packet)
            #self._timer.cancel()
            self._timer_list[seq_num][0] = Timer(5.0, self.time_out, args=(my_socket, seq_num,))
            self._timer_list[seq_num][0].start()
            my_socket.sendto(send_packet.encode(), (self._destination_address, self._destination_port))

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

        packet += bin(seq_num)[2:].zfill(8)

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
        seq_num = int(recv[48:56], 2)
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

    def dummy_method(self):
        print("DUMMY METHOD")