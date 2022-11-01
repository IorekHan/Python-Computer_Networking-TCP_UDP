from socket import *

address = ('127.0.0.1', 7777)

s = clientSocket = socket(AF_INET,SOCK_DGRAM)
message = ''
s.sendto(''.encode(),address)

while True:

    data, addr = s.recvfrom(1024) 
    data = data.decode()

    print('Question: ', data)
    print('')
    print('Answer:')
    print('')

    Answer = input('')
    s.sendto(Answer.encode(), address)

    if data == "Green Pass" or data == "Red Pass":
        print(data)
        break

clientSocket.close()
