#coding: UTF-8
import sys
import hashlib
sys.path.append('./lib/dpkt-1.7/')
import dpkt

class TCP_STREAM:
        def __init__(self):
            '''stream init...
               streams= {
                         'id_1':  {
                                    'c_ip':
                                    's_ip':
                                    'c_port':
                                    's_port':
                                    'c_des':,
                                    'c_packets':[{
                                                   'ts': , 
                                                   'id': , 
                                                   'src': , 
                                                   'dst': , 
                                                   'sport': ,
                                                   'dport': ,
                                                   'flags': ,
                                                   'seq': ,
                                                   'ack': ,
                                                   'data_len',
                                                   'win': }, {},{},... ,{...}],
                                    's_des':,
                                    's_packets':[{
                                                   'ts': , 
                                                   'id': , 
                                                   'src': , 
                                                   'dst': , 
                                                   'sport': ,
                                                   'dport': ,
                                                   'flags': ,
                                                   'seq': ,
                                                   'ack': ,
                                                   'data_len',
                                                   'win': }, {},{},... ,{...}],
                                    'data_len':,
                                    'statt_time':,
                                    'end_time':
                                    'http':[{
                                              'request':{'method':, 'uri':, 'headers':}
                                              'respones':{'status':, 'reason':, 'headers':}
                                             }, {}]
                                    }, {},{},... ,{...}],
                                    },
                        'id_2':   {...},
                               ...,
                        'id_x':   {...}}
            '''
            self.streams = {} 
            self.http_req = dpkt.http.Request
            self.http_res = dpkt.http.Response

        def http(self, pkt, stream, data_len, http_type, ts):
            if data_len <= 0: 
                return

            sindex = len(stream['s_packets'])
            pointer = 0
            try:
                msg = http_type(pkt, pointer)
            except dpkt.Error, error: # if the message failed
                if pointer == 0: # if this is the first message
                    #print('Invalid http: %s' % error)
                    return
                else: # we're done parsing messages
                    #print("We got a dpkt.Error %s, but we are done." % error)
                    #break # out of the loop
                    return
            except:
                print("Unkown error.")
                return
            # ok, all good
            if http_type == dpkt.http.Request:
                '''client > server'''
                http = {}
                http['request'] = {} 
                http['request']['uri'] = msg.uri
                http['request']['method'] = msg.method
                http['request']['headers'] = msg.headers
                http['request']['index'] = sindex 
                http['request']['ts'] = ts 
                stream['http'].append(http)
            else:
                '''server > client'''
                i = len(stream['http']) - 1
                if len(stream['http']) == 0:
                    i = 0
                    http = {}
                    stream['http'].append(http)
                else:
                    http = stream['http'][i]
                http['response'] = {}
                http['response']['status'] = msg.status
                http['response']['reason'] = msg.reason
                http['response']['headers'] = msg.headers
                http['response']['index'] = sindex 
                http['response']['ts'] = ts 


        def add(self, ts, ippkt, tcppkt):
            if isinstance(tcppkt, dpkt.tcp.TCP): #TCP
                    dst = '%d.%d.%d.%d' % tuple(map(ord, list(ippkt.dst)))
                    src = '%d.%d.%d.%d' % tuple(map(ord, list(ippkt.src)))
                    des = src + ":" + str(tcppkt.sport) + " -> " + dst + ":" + str(tcppkt.dport)
                    des_revert = dst + ":" + str(tcppkt.dport) + " -> " + src + ":" + str(tcppkt.sport)
                    packet = {}
                    packet['ts'] = ts
                    packet['ttl'] = ippkt.ttl 
                    packet['src'] = src
                    packet['dst'] = dst
                    packet['id'] = ippkt.id
                    packet['sport'] = tcppkt.sport
                    packet['dport'] = tcppkt.dport
                    packet['flags'] = tcppkt.flags
                    packet['seq'] = tcppkt.seq
                    packet['ack'] = tcppkt.ack
                    packet['win'] = tcppkt.win 
                    packet['data_len'] = ippkt.len - tcppkt.__hdr_len__ - len(tcppkt.opts) - ippkt.__hdr_len__
                    #print 'len of tcppkt.data: ' + str(len(tcppkt.data))
                    #print 'value of tcpkt.hdrlen: ' + str(tcppkt.__hdr_len__)
                    #print 'value of ippkt.hdrlen: ' + str(ippkt.__hdr_len__)
                    #print 'len of ippkt.data: ' + str(len(ippkt.data))
                    #print 'value of ippkt.len: ' + str(ippkt.len)
                    stream_id = hashlib.md5(des).hexdigest()
                    stream_id_revert = hashlib.md5(des_revert).hexdigest()

                    if stream_id in self.streams:
                        self.streams[stream_id]['c_packets'].append(packet)
                        self.streams[stream_id]['c_des'] = des
                        self.streams[stream_id]['c_data_len'] += packet['data_len']
                        self.http(tcppkt.data, self.streams[stream_id], packet['data_len'], self.http_req, ts)
                    elif stream_id_revert in self.streams:
                        self.streams[stream_id_revert]['s_packets'].append(packet)
                        self.streams[stream_id_revert]['s_des'] = des_revert
                        self.streams[stream_id_revert]['s_data_len'] += packet['data_len']
                        #init self.streams[stream_id_revert]['c_packets'][0]['ack']
                        if len(self.streams[stream_id_revert]['s_packets']) == 1:
                            self.streams[stream_id_revert]['c_packets'][0]['ack'] = self.streams[stream_id_revert]['s_packets'][0]['seq']
                        self.http(tcppkt.data, self.streams[stream_id_revert], packet['data_len'], self.http_res, ts)
                    else:#new
                       # if packet['flags'] & (dpkt.tcp.TH_SYN | dpkt.tcp.TH_ACK) == (dpkt.tcp.TH_SYN | dpkt.tcp.TH_ACK):
                       #    print 'SYN-ACK'
                       # elif packet['flags'] & (dpkt.tcp.TH_SYN | dpkt.tcp.TH_ACK) == dpkt.tcp.TH_SYN:
                       #    print 'SYN'
                       # elif packet['flags'] & (dpkt.tcp.TH_SYN | dpkt.tcp.TH_ACK) == (dpkt.tcp.TH_SYN | dpkt.tcp.TH_ACK):
                       #    print 'ACK'
                       #    return 
                        if (packet['flags'] & dpkt.tcp.TH_SYN) != dpkt.tcp.TH_SYN:
                            return 
                        self.streams[stream_id] = {} 
                        self.streams[stream_id]['c_ip'] = src
                        self.streams[stream_id]['s_ip'] = dst
                        self.streams[stream_id]['c_port'] = tcppkt.sport 
                        self.streams[stream_id]['s_port'] = tcppkt.dport 
                        self.streams[stream_id]['c_data_len'] = 0 
                        self.streams[stream_id]['s_data_len'] = 0 
                        self.streams[stream_id]['start_time'] = ts
                        self.streams[stream_id]['c_packets'] = []
                        self.streams[stream_id]['s_packets'] = []
                        self.streams[stream_id]['c_packets'].append(packet)
                        self.streams[stream_id]['c_des'] = '' 
                        self.streams[stream_id]['s_des'] = '' 
                        self.streams[stream_id]['http'] = []

