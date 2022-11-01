from socket import*
address = ('127.0.0.1', 7777)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address) 
s.listen(5)

conn, addr = s.accept()  

QI = 'Have you experienced any COVID-19 symptoms in the past 14 days? '
QII = 'Have you been in close contact with anyone who has tested positive for COVID-19 in the past 14 days? '
QIII = 'Have you tested positive for COVID-19 in the past 14 days? '
Qs = [QI,QII,QIII]
green = "Green Pass"
red = "Red Pass"

while True:

	count = 0

	for Q in Qs:

		data = data.strip()
		conn.sendall(Q.encode())
		data = conn.recv(1024)  
		data = data.decode()
		print('Answer', data)
		
		if data == 'Yes':
			count += 1
		

	if count == 0:
		conn.sendall(green.encode())
	else:
		conn.sendall(red.encode())
	break
conn.close()
s.close()
