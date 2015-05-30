#coding: UTF-8
import os
import re
import sys
import json
import hashlib
import StringIO
sys.path.append('./dpkt-1.7/')
import dpkt
sys.path.append('./XlsxWriter-0.7.3/')
import xlsxwriter
#from matplotlib.pyplot import *

class TCP_STREAM:
        def __init__(self):
            '''stream init...
               streams= {
                         'id':{
                            'c_ip':
                            's_ip':
                            'c_port':
                            's_port':
                            'c_des':,
                            'c_packets':[],
                            's_des':,
                            's_packets':[],
                            'data_len':,
                            'statt_time':,
                            'end_time':},
                        'id':{...},
                        ...,
                        'id':{...}}
            '''
            self.streams = {} 
        def add(self, ts, ippkt, tcppkt):
            if isinstance(tcppkt, dpkt.tcp.TCP): #TCP
                    dst = '%d.%d.%d.%d' % tuple(map(ord, list(ippkt.dst)))
                    src = '%d.%d.%d.%d' % tuple(map(ord, list(ippkt.src)))
                    des = src + ":" + str(tcppkt.sport) + " -> " + dst + ":" + str(tcppkt.dport)
                    des_revert = dst + ":" + str(tcppkt.dport) + " -> " + src + ":" + str(tcppkt.sport)
                    packet = {}
                    packet['ts'] = ts
                    packet['src'] = src
                    packet['dst'] = dst
                    packet['id'] = ippkt.id
                    packet['sport'] = tcppkt.sport
                    packet['dport'] = tcppkt.dport
                    packet['flags'] = tcppkt.flags
                    packet['seq'] = tcppkt.seq
                    packet['ack'] = tcppkt.ack
                    packet['win'] = tcppkt.win 
                    stream_id = hashlib.md5(des).hexdigest()
                    stream_id_revert = hashlib.md5(des_revert).hexdigest()

                    if stream_id in self.streams:
                        self.streams[stream_id]['c_packets'].append(packet)
                        self.streams[stream_id]['c_des'] = des
                        self.streams[stream_id]['data_len'] += len(tcppkt.data)
                    elif stream_id_revert in self.streams:
                        self.streams[stream_id_revert]['s_packets'].append(packet)
                        self.streams[stream_id_revert]['s_des'] = des_revert
                        self.streams[stream_id_revert]['data_len'] += len(tcppkt.data)
                    else:#new
                        self.streams[stream_id] = {} 
                        self.streams[stream_id]['c_ip'] = src
                        self.streams[stream_id]['s_ip'] = dst
                        self.streams[stream_id]['c_port'] = tcppkt.sport 
                        self.streams[stream_id]['s_port'] = tcppkt.dport 
                        self.streams[stream_id]['data_len'] = 0 
                        self.streams[stream_id]['start_time'] = ts
                        self.streams[stream_id]['c_packets'] = []
                        self.streams[stream_id]['s_packets'] = []
                        self.streams[stream_id]['c_packets'].append(packet)

class PCAP_PARSE:
        def __init__(self):
            '''parse pcap init some parameters
            '''
            self.stream = TCP_STREAM()

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

parse = PCAP_PARSE()

class ANALYSIS_TCP:
        def __init__(self, file_name, streams_info):
            '''analysis init...
            '''
            self.xlsx = xlsxwriter.Workbook(file_name + '.xlsx')
            self.streams = streams_info
            self.timeformat = self.xlsx.add_format()
            self.timeformat.set_num_format('0.00000000')

        def seq_ack_time(self):
            sheet = self.xlsx.add_worksheet('seq_ack')

            for id in self.streams:
                sheet.write('A1', 'seqtime')
                sheet.write('A2', 'seq')
                sheet.write('A1', 'acktime')
                sheet.write('A2', 'ack')
                seq = [self.streams[id]['s_packets'][i]['seq']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['s_packets']))]
                ack = [self.streams[id]['c_packets'][i]['ack']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['c_packets']))]
                seqtime = [self.streams[id]['s_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['s_packets']))]
                acktime = [self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['c_packets']))]
                ack[0] = 0
                sheet.write_row('B1', seqtime, self.timeformat)
                sheet.write_row('B2', seq)
                sheet.write_row('B3', acktime, self.timeformat)
                sheet.write_row('B4', ack)

            #chart
            chart = self.xlsx.add_chart({'type': 'line'})
            chart.add_series({
                    'categories': '=seq_ack!$B$2:$QVS$2',
                    'values':     '=seq_ack!$B$1:$QVS$1',
                    'line':       {'color': 'red'},
            })
            chart.add_series({
                    'categories': '=seq_ack!$B$4:$HXS$4',
                    'values':     '=seq_ack!$B$3:$HXS$3',
                    'line':       {'color': 'blue'},
            })

            chart2 = self.xlsx.add_chart({'type': 'line'})
            chart2.add_series({
                    'categories': '=seq_ack!$B$1:$QVS$1',
                    'values':     '=seq_ack!$B$2:$QVS$2',
                    'line':       {'color': 'red'},
            })
            chart2.add_series({
                    'categories': '=seq_ack!$B$3:$HXS$3',
                    'values':     '=seq_ack!$B$4:$HXS$4',
                    'line':       {'color': 'blue'},
            })
            #chart.set_size({'width': 720, 'height': 576})
            sheet.insert_chart('B6', chart)
            sheet.insert_chart('J6', chart2)

        def save_work(self):
            self.xlsx.close()


if __name__ == '__main__':
    cap_file = sys.argv[1]
    if not os.path.exists(cap_file):
        print cap_file + " not exist"
        exit()

    f = file(cap_file)
    #f = file("/home/lewis/work/tmp/xx.cap")
    parse.collect_streams(f)
    print parse.stream.streams

    file = open('./stream.json', "ab")
    json.dump(parse.stream.streams, file)

    analysis = ANALYSIS_TCP(cap_file, parse.stream.streams)
    analysis.seq_ack_time()
    analysis.save_work()


   # stream = {}
   # for stream in streams:
   #     time1 = [seq[0] for seq in stream['seq']]
   #     seq = [seq[1] for seq in stream['seq']]

   #     if len(seq) < 10:
   #         continue

   #     des1 = stream['src'] + ":" + str(stream['sport']) + " -> " + stream['dst'] + ":" + str(stream['dport'])
   #     des2 = stream['dst'] + ":" + str(stream['dport']) + " -> " + stream['src'] + ":" + str(stream['sport'])
   #     stream_id = hashlib.md5(des2).hexdigest()
   #     print stream['stream_id']
   #     stream = parse.search_stream(streams, stream_id)
   #     if stream == False:
   #         continue
   #     time2 = [ack[0] for ack in stream['ack']]
   #     ack = [ack[1] for ack in stream['ack']]
   #     win = [win[1] for win in stream['win']]

   #     ##remove zero value
   #     if seq[0] == 0:
   #         seq[0] = seq[1]
   #         time1[0] = time1[1]
   #     if ack[0] == 0:
   #         ack[0] = ack[1]
   #         time2[0] = time2[1]

   #     ##skip server(only send data) direction package
   #     if ack[1] == ack[len(ack)/2]:
   #         continue

   #     ##outstanding bytes
   #     i = 0
   #     send = 0
   #     acked = 0
   #     flight = []
   #     while i < len(seq):
   #         if send < seq[i]:
   #             send = seq[i] 

   #         j = 0 
   #         for time in time2:
   #             if time > time1[i]:
   #                break
   #             j = j + 1
   #         
   #         if j == len(time2):
   #             j = j - 1
   #         if acked < ack[j]:
   #             acked = ack[j]
   #         flight.append(send - acked) 
   #         i = i + 1 

   #    # ##sent/ack 
   #    # grid(True)
   #    # ylabel('seqno', fontdict={'fontsize':20})
   #    # xlabel('time(s)', fontdict={'fontsize':20})
   #    # plot(time1, seq, 'ro:', linewidth=2, label='sent ' + des1)
   #    # plot(time2, ack, 'go:', linewidth=2, label='acked ' + des2)
   #    # legend(title=cap_file, loc='best')
   #    # #savefig('ack_timestamp.png')
   #    # show()

   #    # ##receive windows
   #    # grid(True)
   #    # ylabel('windows', fontdict={'fontsize':20})
   #    # xlabel('time(s)', fontdict={'fontsize':20})
   #    # plot(time2, win, 'y-o', linewidth=2, label='win time(s) ' + des1)
   #    # legend(title=cap_file +'(windows)', loc='best')
   #    # #savefig('ack_timestamp.png')
   #    # show()

   #    # ##outstanding bytes
   #    # grid(True)
   #    # ylabel('outstanding', fontdict={'fontsize':20})
   #    # xlabel('time(s)', fontdict={'fontsize':20})
   #    # plot(time1, flight, 'y-o', linewidth=2, label='outstanding time(s) ' + des1)
   #    # legend(title=cap_file+ '(outstanding)', loc='best')
   #    # #savefig('ack_timestamp.png')
   #    # show()
