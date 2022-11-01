from socket import*

address = ('127.0.0.1', 7777)
s = serverSocket = socket(AF_INET, SOCK_DGRAM)
s.bind((address))
print("The server is ready to receive")

QI='Have you experienced any COVID-19 symptoms in the past 14 days? '
QII='Have you been in close contact with anyone who has tested positive for COVID-19 in the past 14 days? '
QIII='Have you tested positive for COVID-19 in the past 14 days? '
Qs = [QI,QII,QIII]
greenpass = 'Green Pass'
redpass = 'Red Pass'

while True:

	data, addr = s.recvfrom(1024)
	
	count = 0

	for Q in Qs:
		
		while True:
			message, clientAdress = serverSocket.recvfrom(1024)
			modifiedMessage = message.decode().upper()
			serverSocket.sendto(Q.encode(),clientAdress)
			modifiedMessage = message.decode()
			s.sendto(Q.encode(),addr)
			data, addr = s.recvfrom(1024) 
			data = data.decode()
		if (modifiedMessage.lower() == 'yes'):
			count += 1

		if count == 0:
			s.sendto(greenpass.encode(),addr)
		else:
		    s.sendto(redpass.encode(),addr)
	break

serverSocket.sendto(response.encode(),clientAdress)
