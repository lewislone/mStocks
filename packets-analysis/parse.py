#coding: UTF-8
import sys
import stream
#from matplotlib.pyplot import *
sys.path.append('./lib/dpkt-1.7/')
import dpkt

class PCAP_PARSE:
        def __init__(self):
            '''parse pcap init some parameters
            '''
            self.stream = stream.TCP_STREAM()

        def collect_streams(self, pcap):
            reader = dpkt.pcap.Reader(pcap)

            #Determine the packet type.
            if (reader.datalink() == dpkt.pcap.DLT_EN10MB): #normal ethernet
              PacketClass = dpkt.ethernet.Ethernet
              print 'ethernet' 
            elif (reader.datalink() == dpkt.pcap.DLT_LINUX_SLL): #ssl: capture by "--any" option
              PacketClass = dpkt.sll.SLL
              print 'SLL' 
            elif reader.datalink() == 0: #Loopback packet
              PacketClass = dpkt.loopback.Loopback
              print 'Loopback' 
            elif reader.datalink() == 101: #RAW packet
              PacketClass = None
              print 'Raw' 
            else:
              print 'unknown packet type!!' 
              return

            for ts, buf in reader:
                if PacketClass:
                    packet = PacketClass(buf)
                    ippkt = packet.data
                else:
                    packet = dpkt.ip.IP(buf)
                    ippkt = packet
                #dst = '%d.%d.%d.%d' % tuple(map(ord, list(ippkt.dst)))
                #src = '%d.%d.%d.%d' % tuple(map(ord, list(ippkt.src)))
                #print str(ts) + ": " + src + " -> " + dst 

                try:
                    if isinstance(ippkt, dpkt.ip.IP):
                        if isinstance(ippkt.data, dpkt.tcp.TCP): #TCP
                            tcppkt = ippkt.data
                            self.stream.add(ts, ippkt, tcppkt)
                        else:
                            print("it is not a tcp packet!!!")
                            continue
                    else:
                        print("it is not a ip packet!!!")
                        continue
                except dpkt.Error, error:
                        print(error)
                        return

