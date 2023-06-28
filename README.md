# Computer Network
  
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

The following are introductions about UDP clients and servers code:

## UDP Client & Server
![image](https://user-images.githubusercontent.com/116987376/199144275-b89bf64f-baf4-43ef-bf7e-3362bcb85815.png)

## TCP UDP difference
This project set TCP connections upon UDP connections.
#### TCP has an additional handshake to the server side (sender side) to set up the connection.
#### TCP makes sure that every message is received by the receiver, if it's not, send again.
Which means UDP datagrams can be lost through internet transactions and the sender will never resend it because the sender never knows.

