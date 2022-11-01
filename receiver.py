import socket
import sys
import segments
import struct
import datetime

Maxpayload = 556

try:
  recvfilename = sys.argv[1]
  portListen = int(sys.argv[2])
  sourceIP = socket.gethostbyname(sys.argv[3])
  sourceport = int(sys.argv[4])
  logfile = sys.argv[5]

except IndexError:
  exit("Please input: $ Receiver.py [recvfilename] [portListen] [sourceIP] [sourceport] [logfile] ")

  print (recvfilename + ", " + portListen + ", " + str(sourceIP) + ", " + str(sourceport) + ", " + logfile + ". ")

except TypeError:
  exit("Please input: $ Receiver.py [recvfilename] [portListen] [sourceIP] [sourceport] [logfile] ")

  print (recvfilename + ", " + portListen + ", " + str(sourceIP) + ", " + str(sourceport) + ", " + logfile + ". ")


try:

# Socket & file

  #UDP socket
  recvIP = socket.gethostname()
  recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  recvSocket.bind((recvIP, portListen))

  ACKsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  ACKsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)


  try:
    recvfileMark = open(recvfilename, 'w')
  except IOError:
    print(recvfilename + " was not found.")
    ACKsocket.close()
    recvSocket.close()
    sys.exit()

  # write channel for the logfile
  if logfile == "stdout":
    logfileMark = sys.stdout
  else:
    try:
      logfileMark = open(logfile,'w')
    except IOError:
      print(logfile + " was not found.")
      ACKsocket.close()
      recvSocket.close()
      sys.exit()



  # sequence of packets expected
  expected_seq_number = 0

  while True:
      try:
        packet, addr = recvSocket.recvfrom(576)

        if packet:

          #unpack packet
          sourcePort, destPort,pktSeq, ACKnum, HeaderL, final, ack, checksum, payload = segments.unpack_segment(packet)


          if(str(checksum).rstrip(' \t\r\n\0') == str(segments.checksum_function(sourcePort, destPort, pktSeq, ACKnum, final, ack, payload)).rstrip(' \t\r\n\0')):

            if(pktSeq == expected_seq_number):

 
              if final:
                recvfileMark.write(payload.rstrip(' \t\r\n\0'))
                ReceptionT = datetime.datetime.now()
                logfileMark.write(str(ReceptionT) + " | source port: " + str(sourcePort) + " | destination port: " + str(destPort) + " | sequence number: " + str(pktSeq) + " | ack number: " + str(ACKnum) + " | " + "ACK: 0 | FIN: " + str(final) + " RECEIVED\n")


              else:
                recvfileMark.write(payload)
                ReceptionT = datetime.datetime.now()
                logfileMark.write(str(ReceptionT) + " | source port: " + str(sourcePort) + " | destination port: " + str(destPort) + " | sequence number: " + str(pktSeq) + " | ack number: " + str(ACKnum) + " | " + "ACK: 0 | FIN: " + str(final) + " RECEIVED\n")
             

              
              logfileMark.write(str(ReceptionT) + " | source port: " + str(sourcePort) + " | destination port: " + str(destPort) + " | sequence number: " + str(pktSeq) + " | ack number: " + str(ACKnum) + " | " + "ACK: 1 | FIN: " + str(final) + " ACK SENT\n")
              expected_seq_number += 1
              ACKsocket.sendto(str(ACKnum),(sourceIP,sourceport))


      except KeyboardInterrupt:
        recvSocket.close()
        sys.exit()

  print ("exited inner loop")

except KeyboardInterrupt:
  print (" , CTRL + C command issued, sender socket closing ----------")
  recvSocket.close()
  ACKsocket.close()
  sys.exit()
