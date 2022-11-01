-This program works with python and newudpl  
-The program contains: segment.py, sender.py and receiver.py.  
  
## I. The TCP Segment Structure  
I used the Standard TCP Header to pack and unpack the payload of my packets. In other words, all my
packets had 20 Byte headers that represented the packet's source port (2 bytes), destination port (2 bytes),
sequence number (4 bytes), acknowledgement number (4 bytes), header size (1 byte), flags (1 byte), window
size (2 bytes), checksum (2 bytes), urgent pointer (2 bytes)  
  
## II. The states typically visited by a sender and receiver
My code works by first having both the sender and receiver setting up the receiving and destination sockets,
as well as setting up other descriptors like log files and the original file which will be reconstructed from the
packets sent by the sender to the receiver. Sender then divides the original file into segments and stores them
in a tuple (or array) from which it will send later on. It then uses the UDP sockets to send them to the receiving
side, only moving on to the next ones when an ack sent from the receiving side has been received. Once all
the packets are sent, the sending side receives the statistics of the code (as specified in the original
assignment)  
  
## III. Loss Recovery mechanism
Each packet has its own timer (whose timeout limit is always updated through the TCP estimated RTT
formulas, regardless if the packet gets ack or not). If an ack is received within the timeout window, its reception
is logged at the sending side and prompts the next packets to be sent. However if an ACK is not received in
the timeout window, my code calls the method send_packet_w_acks yet again to repeat this process.
The following is a experiment, the test codes in terminal are
```
Emulator: ./newudpl -vv -o ‘localhost’:8111 -i ‘localhost’:’*’ -L 10 -B 50 -O 50 -d 0.8
Receiver: python3 Receiver.py recvfile.txt 8111 localhost 8112 logfile.txt
Sender: python3 Sender.py sendfile.txt localhost 41192 8112 logfile.txt 1
```
