#coding: UTF-8
import sys
sys.path.append('./lib/dpkt-1.7/')
import dpkt
sys.path.append('./lib/XlsxWriter-0.7.3/')
import xlsxwriter

class SUM:
        def __init__(self, streams_info, xlsx):
            self.xlsx = xlsx
            self.streams = streams_info
            self.mini_rto = 0.2
            self.default = self.xlsx.add_format()
            self.catalog_format = self.xlsx.add_format({'bold': True, 'font_color': 'blue'})
            self.catalog_format.set_align('center')
            self.uncomplete_format = self.xlsx.add_format({'bg_color': 'red'})

        def search_in_box(self, box, pos, len):
            ret = 0
            for item in box:
                if not (pos+len <= item[1] or pos >= item[1]+item[2]):
                    ret = 1
                    break
            return ret

        def checkRTO(self, acktime, ack, ts, seq):
            i = 0
            ret = 0
            n = len(acktime) 
            while i < n:
                if acktime[i] >= ts:
                    break
                elif ack[i] == seq:
                    if (ts-acktime[i]) >= self.mini_rto:
                        ret = 1
                        break
                i = i + 1

            return ret


        def retransmit(self, stream, seq, seqtime, ack, acktime):
            '''retransmit bytes'''

            ret = {}
            i, j = 0, 0
            minirtt, maxrtt = 0, 0
            send, acked = 0, 0
            lastseq, lastack = 1, 0
            dupack = 0
            retransmit = 0
            complete = 0
            firstdata = 0
            ofo = []
            rto = []
            re = []
            syn_re = []
            rtt = []
            init_cwnd = []
            len_ack = len(ack)
            len_seq = len(seq)
            while i < len_ack:
                while j < len_seq:
                    if acktime[i] < seqtime[j]:
                        break
                    ###send data likeness
                    #retransmint
                    if lastseq == seq[j] or lastseq == lastack:
                        lastseq = seq[j] + stream['s_packets'][j]['data_len']
                    elif lastack > lastseq:
                        lastseq = lastack
                    else:
                        if seq[j]+stream['s_packets'][j]['data_len'] <= lastseq or self.search_in_box(ofo, seq[j], stream['s_packets'][j]['data_len']): #re
                            #print (lastseq, seq[j])
                            if self.checkRTO(acktime, ack, seqtime[j], seq[j]) == 1:
                                rto.append([seqtime[j], seq[j], stream['s_packets'][j]['data_len']])
                            else:
                                re.append([seqtime[j], seq[j], stream['s_packets'][j]['data_len']])
                            if stream['s_packets'][j]['flags'] & dpkt.tcp.TH_SYN:
                                syn_re.append([seqtime[j], seq[j], stream['s_packets'][j]['data_len']])
                        else:
                            ofo.append([seqtime[j], seq[j], stream['s_packets'][j]['data_len']])

                    #init cwnd
                    if firstdata == 0 and stream['s_packets'][j]['data_len'] > 0:
                       firstdata = j 
                    if firstdata != 0 and seqtime[j] - seqtime[firstdata] < 0.001:#assume send one cwnd packet in 1ms
                       init_cwnd.append(str(stream['s_packets'][j]['data_len']))
                    j = j + 1

                ###receive ack likeness
                #3 hands shake
                if (stream['c_packets'][i]['flags'] & (dpkt.tcp.TH_ACK)) == dpkt.tcp.TH_ACK \
                        and stream['c_packets'][i]['seq']-stream['c_packets'][0]['seq'] == 1 \
                        and stream['c_packets'][i]['data_len'] == 0:
                        complete = 1
                #duplicate ack
                if lastack < ack[i]:
                    lastack = ack[i]
                elif lastack <= ack[i]:
                    dupack += 1
                    if stream['c_packets'][i]['flags'] & dpkt.tcp.TH_SYN:
                        syn_re.append([acktime[i], ack[i], stream['c_packets'][i]['data_len']])
                #rtt
                k = 0 
                while k < j:
                      if seq[k] <= ack[i]-1 and ack[i]-1 <= seq[k]+stream['s_packets'][k]['data_len']:
                         rtt.append([acktime[i], acktime[i] - seqtime[k]])
                         if acktime[i] - seqtime[k] > maxrtt:
                            maxrtt = acktime[i] - seqtime[k]
                         if minirtt == 0:
                            minirtt = acktime[i] - seqtime[k]
                         if minirtt > acktime[i] - seqtime[k]:
                            minirtt = acktime[i] - seqtime[k]
                      k = k + 1

                i = i + 1

            ret['initcwnd'] = ';'.join(init_cwnd)
            ret['rtt'] = rtt 
            ret['rto'] = len(rto) 
            ret['re'] = len(re) 
            ret['ofo'] = len(ofo) 
            ret['dupack'] = dupack 
            ret['minirtt'] = minirtt 
            ret['maxrtt'] = maxrtt 
            ret['syn_re'] = len(syn_re)
            ret['complete'] = complete 
            return ret 

        def start(self):
            print '###'
            print 'start case: SUM :)'
            sheet = self.xlsx.add_worksheet('sum')
            #catalog
            sheet.set_column(0, 0, 45) #set A column's width to 40
            sheet.write('A1', 'stream', self.catalog_format)
            sheet.write('B1', 'datalen', self.catalog_format)
            sheet.write('C1', 'time', self.catalog_format)
            sheet.write('D1', 'synrtt', self.catalog_format)
            sheet.write('E1', 'TTFB', self.catalog_format)
            sheet.write('F1', 'retran', self.catalog_format)
            sheet.write('G1', 'rto', self.catalog_format)
            sheet.write('H1', 'dupack', self.catalog_format)
            sheet.write('I1', 'maxrtt', self.catalog_format)
            sheet.write('J1', 'minirtt', self.catalog_format)
            sheet.write('K1', 'dupsyn', self.catalog_format)
            sheet.set_column(11, 11, 45) #set A column's width to 40
            sheet.write('L1', 'inicwnd', self.catalog_format)
            #sheet.write('I1', 'ishttp')
            #sheet.write('I1', 'isKeepLive')
            #sheet.write('J1', 'url')

            index = 2 
            for id in self.streams:
                if len(self.streams[id]['c_packets']) <= 1 or len(self.streams[id]['s_packets']) <= 1:
                    continue
                seq = [self.streams[id]['s_packets'][i]['seq']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['s_packets']))]
                ack = [self.streams[id]['c_packets'][i]['ack']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['c_packets']))]
                data_len = [self.streams[id]['s_packets'][i]['data_len'] for i in range(0, len(self.streams[id]['s_packets']))]
                seqtime = [self.streams[id]['s_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['s_packets']))]
                acktime = [self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['c_packets']))]

                c_len = len(self.streams[id]['c_packets'])
                s_len = len(self.streams[id]['s_packets'])
                sheet.write('A'+str(index), self.streams[id]['c_des'])
                sheet.write('B'+str(index), self.streams[id]['s_data_len'])

                #time
                timecost = 0
                i = c_len - 1
                while i > 0: 
                    if self.streams[id]['c_packets'][i]['flags'] & (dpkt.tcp.TH_FIN|dpkt.tcp.TH_RST) != 0:
                       timecost = self.streams[id]['c_packets'][i]['ts'] - self.streams[id]['start_time']
                       break
                    i -= 1
                if timecost == 0:
                    timecost = self.streams[id]['c_packets'][c_len-1]['ts'] - self.streams[id]['start_time']
                sheet.write('C'+str(index), timecost)
                #synrtt
                i = 0
                while i < c_len: 
                    if self.streams[id]['c_packets'][i]['flags'] & dpkt.tcp.TH_ACK:
                        sheet.write('D'+str(index), self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'])
                        break
                    i += 1
                #TTFB
                i = 0
                first_data_time = 0
                get_data_time = 0
                while i < s_len: 
                    if self.streams[id]['s_packets'][i]['data_len'] != 0 and not (self.streams[id]['s_packets'][i]['flags'] & dpkt.tcp.TH_SYN):
                        first_data_time = self.streams[id]['s_packets'][i]['ts']
                        break
                    i += 1
                i = 0
                while i < c_len: 
                    if self.streams[id]['c_packets'][i]['flags'] & dpkt.tcp.TH_ACK:
                        try:
                            get_data_time = self.streams[id]['c_packets'][i+1]['ts']
                        except:
                            get_data_time = self.streams[id]['c_packets'][i]['ts']
                        break
                    i += 1
                sheet.write('E'+str(index), first_data_time - get_data_time)
                ##analysis
                result = self.retransmit(self.streams[id], seq, seqtime, ack, acktime)
                #retransmit
                sheet.write('F'+str(index), result['re'])
                #rto(rot==0.2s)
                sheet.write('G'+str(index), result['rto'])
                #dupack
                sheet.write('H'+str(index), result['dupack'])
                #maxrtt
                sheet.write('I'+str(index), result['maxrtt'])
                #minirtt
                sheet.write('J'+str(index), result['minirtt'])
                #syn retransmint
                sheet.write('K'+str(index), result['syn_re'])
                #initcwnd
                sheet.write('L'+str(index), result['initcwnd'])
                if result['complete'] == 0:
                    sheet.set_row(index,15,self.uncomplete_format)

                ##http
                sheet.write('M1', 'code', self.catalog_format)
                sheet.write('N1', 'host', self.catalog_format)
                sheet.write('O1', 'uri', self.catalog_format)
                sheet.set_column(13, 13, 20) #set A column's width to 40
                if len(self.streams[id]['http']) > 0:
                    i = 0
                    while i < len(self.streams[id]['http']):
                            if self.streams[id]['http'][i].has_key('response'):
                                sheet.write('M'+str(index+i), self.streams[id]['http'][i]['response']['status'])
                            if self.streams[id]['http'][i].has_key('request'):
                                if self.streams[id]['http'][i]['request']['method'] == "GET" \
                                        or self.streams[id]['http'][i]['request']['method'] == "POST":
                                    x = self.streams[id]['http'][i]['request']['index']
                                    get_data_time = self.streams[id]['http'][i]['request']['ts']
                                    while x < len(seq):
                                        if self.streams[id]['s_packets'][x]['data_len'] > 0:
                                            first_data_time = self.streams[id]['s_packets'][x]['ts']
                                            print (len(seqtime), self.streams[id]['http'][i]['request']['index'], x)
                                            break
                                        x = x + 1
                                    #TTFB
                                    sheet.write('E'+str(index+i), first_data_time - get_data_time)
                                #uri    
                                sheet.write('O'+str(index+i), self.streams[id]['http'][i]['request']['uri'])
                                if self.streams[id]['http'][i]['request']['headers'].has_key('host'):
                                    #host
                                    sheet.write('N'+str(index+i), self.streams[id]['http'][i]['request']['headers']['host'])
                            i = i + 1
                    index = index + i - 1 

                index = index + 1
    
            print 'finish case: SUM :)'
