#coding: UTF-8
import sys
import hashlib
sys.path.append('./lib/dpkt-1.7/')
import dpkt

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
