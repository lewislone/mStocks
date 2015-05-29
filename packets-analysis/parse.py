#coding: UTF-8
import os
import re
import sys
import json
import dpkt
import hashlib
import StringIO
#from matplotlib.pyplot import *

class PARSE_PCAP:
        def __init__(self):
            '''init some parameters'''
            self.streams = []

        def search_stream(self, streams, id):
            for stream in streams:
                if stream['stream_id'] == id:
                   return stream

            return False 

        def collect_tcp(self, pcap):
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

            print reader
            return
            for ts, buf in pcap:
                new = 0;
                try:
                        eth = dpkt.ethernet.Ethernet(buf)
                        #print ts

                        ##ssl: capture by "--any" option
                        if eth.data.__class__.__name__=='str':
                            eth = dpkt.ethernet.Ethernet(buf[2:])
                        
                        if eth.data.__class__.__name__=='IP':
                            dst = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.dst)))
                            src = '%d.%d.%d.%d' % tuple(map(ord, list(eth.data.src)))
                            id = eth.data.id 
                            #ip = dpkt.ip.IP(eth.data)
                            #print src + " -> " + dst 
                except Exception:
                    print 'ip exception'
                    continue

                try:
                        if eth.data.data.__class__.__name__=='TCP':
                            #tcp = dpkt.tcp.TCP(eth.data.data)
                            tcp = eth.data.data
                            des = src + ":" + str(tcp.sport) + " -> " + dst + ":" + str(tcp.dport)
                            #print des
                            stream_id = hashlib.md5(des).hexdigest()
                            stream = self.search_stream(streams, stream_id)
                            if stream is False:
                                stream = {}
                                stream['stream_id'] = stream_id 
                                stream['id'] = id 
                                stream['src'] = src
                                stream['dst'] = dst
                                stream['sport'] = tcp.sport
                                stream['dport'] = tcp.dport
                                stream['flags'] = tcp.flags
                                stream['seq'] = [] 
                                stream['ack'] = [] 
                                stream['win'] = [] 
                                new = 1
                            stream['win'].append((ts, tcp.win))
                            stream['seq'].append((ts, tcp.seq))
                            stream['ack'].append((ts, tcp.ack))
                except Exception:
                    print 'tcp exception'
                    continue

                if new == 1:
                    streams.append(stream)

            return streams

parse = PARSE_PCAP()

if __name__ == '__main__':
    cap_file = sys.argv[1]
    if not os.path.exists(cap_file):
        print cap_file + " not exist"
        exit() 

    #f = file(cap_file)
    f = file("/home/lewis/work/tmp/xx.cap")
    streams = parse.collect_tcp(f)
    exit()


    file = open('./stream.json', "ab")
    a = {'streams': streams}
    json.dump(streams, file)

    stream = {}
    for stream in streams:
        time1 = [seq[0] for seq in stream['seq']]
        seq = [seq[1] for seq in stream['seq']]

        if len(seq) < 10:
            continue

        des1 = stream['src'] + ":" + str(stream['sport']) + " -> " + stream['dst'] + ":" + str(stream['dport'])
        des2 = stream['dst'] + ":" + str(stream['dport']) + " -> " + stream['src'] + ":" + str(stream['sport'])
        stream_id = hashlib.md5(des2).hexdigest()
        print stream['stream_id']
        stream = parse.search_stream(streams, stream_id)
        if stream == False:
            continue
        time2 = [ack[0] for ack in stream['ack']]
        ack = [ack[1] for ack in stream['ack']]
        win = [win[1] for win in stream['win']]

        ##remove zero value
        if seq[0] == 0:
            seq[0] = seq[1]
            time1[0] = time1[1]
        if ack[0] == 0:
            ack[0] = ack[1]
            time2[0] = time2[1]

        ##skip server(only send data) direction package
        if ack[1] == ack[len(ack)/2]:
            continue

        ##outstanding bytes
        i = 0
        send = 0
        acked = 0
        flight = []
        while i < len(seq):
            if send < seq[i]:
                send = seq[i] 

            j = 0 
            for time in time2:
                if time > time1[i]:
                   break
                j = j + 1
            
            if j == len(time2):
                j = j - 1
            if acked < ack[j]:
                acked = ack[j]
            flight.append(send - acked) 
            i = i + 1 

       # ##sent/ack 
       # grid(True)
       # ylabel('seqno', fontdict={'fontsize':20})
       # xlabel('time(s)', fontdict={'fontsize':20})
       # plot(time1, seq, 'ro:', linewidth=2, label='sent ' + des1)
       # plot(time2, ack, 'go:', linewidth=2, label='acked ' + des2)
       # legend(title=cap_file, loc='best')
       # #savefig('ack_timestamp.png')
       # show()

       # ##receive windows
       # grid(True)
       # ylabel('windows', fontdict={'fontsize':20})
       # xlabel('time(s)', fontdict={'fontsize':20})
       # plot(time2, win, 'y-o', linewidth=2, label='win time(s) ' + des1)
       # legend(title=cap_file +'(windows)', loc='best')
       # #savefig('ack_timestamp.png')
       # show()

       # ##outstanding bytes
       # grid(True)
       # ylabel('outstanding', fontdict={'fontsize':20})
       # xlabel('time(s)', fontdict={'fontsize':20})
       # plot(time1, flight, 'y-o', linewidth=2, label='outstanding time(s) ' + des1)
       # legend(title=cap_file+ '(outstanding)', loc='best')
       # #savefig('ack_timestamp.png')
       # show()
