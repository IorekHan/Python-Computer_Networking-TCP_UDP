import sys
import socket
import struct

HeaderL = 5
Maxpayload = 556

Hformat = 'HHIIBBHHH'

def SEGMENT(sourcePort, destPort, pktSeq, ACKnum, ack, final, Windowsize, payload):

  checksum = checksum_function(sourcePort, destPort, pktSeq, ACKnum, final, ack, payload)

  if final:
    flags = 1
  else:
    flags = 0

  if ack:
    flags += 16

  header = struct.pack(Hformat, sourcePort, destPort, pktSeq, ACKnum, HeaderL, flags, Windowsize, checksum, 0)
  
  segment = header + bytes(payload,encoding='utf-8')
  return segment

def unpack_segment(segment):
  header = segment[:20]

  sourcePort, destPort, pktSeq, ACKnum, HeaderL, flags, Windowsize, checksum, urgent  = struct.unpack(Hformat,header)
  
  ack = 0
  final = 0

  if ((flags >> 4) == 1):
    ack = 1
  else:
    ack = 0

  if (int(flags % 2 == 1)):
    final =  1
  else:
    final = 0

  payload = segment[20:]

  return sourcePort, destPort, pktSeq, ACKnum, HeaderL,  final, ack, checksum, payload


def checksum_function(source_p,dest_p,seq_n,ack_n,final_f,ack_f,payl):
  entire_segment = str(source_p) + str(dest_p) + str(seq_n) + str(ack_n) + str(HeaderL) + str(final_f) + str(ack_f) + payl

  total_sum = 0

  for i in range((0), len(entire_segment) - 1, 2):
    
    current_sum = ord(entire_segment[i]) + (ord(entire_segment[i+1]) << 8)
   
    total_sum = ((total_sum + current_sum) & 0xffff) + ((total_sum + current_sum) >> 16)
  
  return total_sum
