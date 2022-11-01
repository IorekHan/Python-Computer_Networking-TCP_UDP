from socket import*

address = ('127.0.0.1', 7777)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connected to the server")

while True:
    data = s.recv(1024)
    data = data.decode()

    print('Question', data)
    print('Answer',end='')

    if data == "Green Pass" or data == "Red Pass":
        print(data)
        break
    
    Answer = input('')
    s.sendall(Answer.encode())
s.close()
