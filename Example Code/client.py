from socket import *
import fileinput

def parse(recv):
	str_recv = recv[0:-1] #get the file content
	ACK = recv[-1:] #get ACK number
	return str_recv, int.from_bytes(ACK,byteorder='big')

def main():
	serverName = "localhost"
	serverPort = 12020
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	recv_Str = ''
	closingMessage = 'close'
	filename = input("Enter the file you want: ") #'alice.txt'
	seq = '0'
	print("reqesting", filename, "from", serverName)
	f = open(filename, 'wb')
	clientSocket.sendto((filename + seq).encode(),(serverName, serverPort))
	recv, serverAddress = clientSocket.recvfrom(1024)
	recv_Str, ACK = parse(recv)
	if recv_Str == b'OK':
		receiving_status = True
		if int(seq) == ACK:
			if ACK == 0:
				seq = '1'
			else:
				seq = '0'
			clientSocket.sendto(seq.encode(),(serverName, serverPort))
	else:
		clientSocket.sendto((filename + seq).encode(),(serverName, serverPort))
	clientSocket.settimeout(3)
	while receiving_status:
		try:
			recv, serverAddress = clientSocket.recvfrom(1026)
			print('recv:',recv)
			print('len recv:',len(recv))
			recv_Str, ACK = parse(recv)
			print('recv:',recv_Str)
			f.write(recv_Str)
			print("ACK:", ACK)
			if int(seq) == ACK:
				if ACK == 0:
					seq = '1'
				else:
					seq = '0'
				clientSocket.sendto(seq.encode(),(serverName, serverPort))
			else:
				pass
				
			if recv_Str == b'close':
				clientSocket.sendto((closingMessage + seq).encode(),(serverName, serverPort))
				clientSocket.close()
		except timeout:
			print("timed out!")
			clientSocket.sendto(seq.encode(),(serverName, serverPort))

if __name__ == '__main__':
	main()
