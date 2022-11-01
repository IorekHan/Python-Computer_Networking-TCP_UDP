import socket
import sys
import struct
import threading
import datetime
import time

import segments


# Initializing Global Variables ------------------
Buffer = []
Maxsize = 556
Seqnum = 0
TTL = 0.5
RTTdev = 0
RTTest = 0.5
sendfile = ""
logfile = ""
serverIP = ""
serverport = 0
ACKport = 0
SENT = 0
Windowsize = 0
retransSeg = 0



def send_packet_w_acks(send_socket, udpSocket, current_seg):
    send_date_time = datetime.datetime.now()
    send_time = time.time()
    send_socket.sendto(current_seg,(serverIP, serverport))
  
    global TTL, RTTdev, RTTest, SENT, retransSeg

    sourcePort, destPort, pktSeq, ACKnum, HeaderL, Packet, pktACK, Checksum, Payloadsize = segments.unpack_segment(current_seg)
    log_file_descriptor.write(str(send_date_time) + " | source port:"   + str(sourcePort) + "| destination port: "  + str(destPort)+ " | sequence number: " + str(pktSeq) + " | ack number: " + str(ACKnum) + " | " + "ACK: 0 | FIN: " + str(Packet) + " SENT\n")

    try:
        ACKtimestamp = datetime.datetime.now()
        ACKtime = time.time()
        udpSocket.settimeout(TTL)
        ACKnumber = udpSocket.recv(16)
        
        #TTL
        sampleRTT = ACKtime - send_time
        RTTest = RTTest*(0.875) + sampleRTT*(0.125)
        RTTdev = 0.75*(RTTdev) + 0.25*abs(sampleRTT - RTTest)
        TTL = RTTest + 4*RTTdev

    # Successful
        SENT += 1
        log_file_descriptor.write(str(ACKtimestamp) + " | source port: " + str(sourcePort) + " | destination port: " + str(destPort) + " | sequence number: " + str(pktSeq) + " | ack number: " + str(ACKnumber) + " | " + "ACK: 1 | FIN: " + str(Packet) + " RECEIVED\n")

    except socket.timeout:
        log_file_descriptor.write(" source port: " + str(sourcePort) + " | destination port: " + str(destPort) + " | sequence number: " + str(pktSeq) + " | ack number: " + str(ACKnum) + " | " + "ACK: 0 | FIN: " + str(Packet) + "| PACKET DELIVERY WAS UNSUCCESFUL \n")

    #retransmission
        retransSeg += 1
        SENT += 1
        send_packet_w_acks(send_socket, udpSocket, current_seg)

def build_Buffer(sending_fd):

  Seqnum = 0
  ExpectACK = 0

  payloadnow = sending_fd.read(Maxsize)

  while len(payloadnow) > 0:


    #FIN
    if(len(payloadnow) < Maxsize):
      current_segment = segments.SEGMENT(ACKport,serverport,Seqnum,ExpectACK,0,1,Windowsize,payloadnow)
      Buffer.append(current_segment)

    else:
      current_segment = segments.SEGMENT(ACKport,serverport,Seqnum,ExpectACK,0,0,Windowsize,payloadnow)
      Buffer.append(current_segment)


    payloadnow = sending_fd.read(Maxsize)
    Seqnum += 1
    ExpectACK += 1

try:
  sendfile = sys.argv[1]
  serverIP = socket.gethostbyname(sys.argv[2])
  serverport = int(sys.argv[3])
  ACKport = int(sys.argv[4])
  logfile = sys.argv[5]
  Windowsize = int(sys.argv[6])


except IndexError:

  exit("Please input: $ Sender.py [sendfile] [serverIP] [serverport] [ACKport] [logfile] [Windowsize]")

  print ("sendfile + serverIP + str(serverIP) + str(ACKport) + logfile + str(Windowsize) + .")

except TypeError:

    exit ("Please input: $ Sender.py [sendfile] [serverIP] [serverport] [ACKport] [logfile] [Windowsize]")

    print ("sendfile + serverIP + str(serverIP) + str(ACKport) + logfile + str(Windowsize) + .")



try:
  
  sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  #Socket of UDP to be based on
  udpIP = socket.gethostname()
  udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  udpSocket.bind((udpIP , ACKport))

  #TCP channel
  try:
    sending_file_descriptor = open(sendfile,'r')
  except IOError:
    print(sendfile + " was not found.")
    udpSocket.close()
    sending_socket.close()
    sys.exit()

  #Write channel for the logfile
  if logfile == "stdout":
    log_file_descriptor = sys.stdout
  else:
    try:
      log_file_descriptor = open(logfile,'w')
    except IOError:
      print(logfile + " not found.")
      udpSocket.close()
      sending_socket.close()
      sys.exit()

  build_Buffer(sending_file_descriptor)

  while(Seqnum < len(Buffer)):
    send_packet_w_acks(sending_socket,udpSocket, Buffer[Seqnum])
    Seqnum += 1

  # RetansPerc = (float(retransSeg) / SENT)*100
  # print("Delivery Complete -------------------- \n Estimated RTT = " + str(RTTest) + " seonds \n Total bytes sent = " + str(SENT*576) + "\n Segments sent = " + str(SENT) + "\n Retransmitted Segments = " + str(retransSeg) + "\n Segments retransmitted = " + str(RetansPerc) + "%")


except KeyboardInterrupt:
    print (" , CTRL + C command issued, sender socket closing ----------")
    udpSocket.close()
    sending_socket.close()
    sys.exit()
