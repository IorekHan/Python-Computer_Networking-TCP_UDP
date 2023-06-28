# Computer Networking Protocols: UDP, TCP
  
This is a set of programming project in CU CSEE-4119(F2021) Computer Network.

The python files:  
    --segments.py  
    --sender.py  
    --receiver.py
are building a TCP connection with loss recovery mechanism. The TCP connection is built based on a UDP connection, the UDP conneciton system has settings about loss rate and related selections. The UDP simulator is provided by the course and professor. The markdown file:  
    TCP over UDP.md  
is the introduction about the system and codes in the terminal.

The python files:  
    --TCP Client.py   
    --TCP Sercer.py  
    --UDP Client.py  
    --UDP Server.py  
are building client and server using TCP/UDP protocal with python code.

## How to run
Please start Emulator first.
Then Receiver side.
Lastly Sender side.


### Link Emulator codes: 
```cmd
$ ./newudpl -vv -o[sendport]:4000 -i[sendport]:* [FLAGS]

Recommand Flags: -O50 , -B50 , -d0.8 , -L10

Receiver: $ python Receiver.py [receiving_filename(recvfile.txt)] [listening_port] [sender_IP] [sender_port] [log_filename(logfile.txt)]

Sender: $ python Sender.py [sending_filename(sendfile.txt)] [remote_IP] [remote_port] [ack_port] [log_filename(logfile.txt)] [window_size(1)]
```

### Experiment sample code:

Emulator: 
```cmd
./newudpl -vv -o ‘localhost’:8111 -i ‘localhost’:’*’ -L 10 -B 50 -O 50 -d 0.8'''
```
Receiver: 
```cmd
python3 Receiver.py recvfile.txt 8111 localhost 8112 logfile.txt'''
```
Sender: 
```cmd
python3 Sender.py sendfile.txt localhost 41192 8112 logfile.txt 1'''
```






The following are introductions about UDP clients and servers code:

## UDP Client & Server
![image](https://user-images.githubusercontent.com/116987376/199144275-b89bf64f-baf4-43ef-bf7e-3362bcb85815.png)

## TCP UDP difference
This project set TCP connections upon UDP connections.
#### TCP has an additional handshake to the server side (sender side) to set up the connection.
#### TCP makes sure that every message is received by the receiver, if it's not, send again.
Which means UDP datagrams can be lost through internet transactions and the sender will never resend it because the sender never knows.

