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

        def retransmit(self, stream):
            '''retransmit bytes'''
            seq = [stream['s_packets'][i]['seq']-stream['s_packets'][0]['seq'] for i in range(0, len(stream['s_packets']))]
            ack = [stream['c_packets'][i]['ack']-stream['s_packets'][0]['seq'] for i in range(0, len(stream['c_packets']))]
            data_len = [stream['s_packets'][i]['data_len'] for i in range(0, len(stream['s_packets']))]
            seqtime = [stream['s_packets'][i]['ts']-stream['start_time'] for i in range(0, len(stream['s_packets']))]
            acktime = [stream['c_packets'][i]['ts']-stream['start_time'] for i in range(0, len(stream['c_packets']))]

            i = 0
            send = 0
            acked = 0
            lastseq = 0
            lastack = 0
            dupack = 0
            retransmit = 0

            i, j = 0, 0
            ofo = []
            rtt = []
            init_cwnd = []
            len_ack = len(ack)
            len_seq = len(seq)
            while i < len_ack:
                while j < len_seq:
                    if acktime[i] < seqtime[j]:
                        break
                    ###send data likeness
                    #init cwnd
                    if i > 0 and ack[i-1] == 1 and ack[i] != 1 and stream['s_packets'][j]['data_len'] != 0:
                       init_cwnd.append(stream['s_packets'][j]['data_len'])
                    #retransmint
                    if lastseq != seq[j]:
                        ofo.append([seq(j), data_len[j]])
                    else:
                        lastseq = seq[j] + stream['s_packets'][j]['data_len']
                        
                    j = j + 1

                ###receive ack likeness
                #duplicate ack
                if lastack < ack[i]:
                    lastack = ack[i]
                elif lastack <= ack[i]:
                    dupack += 1
                #rtt
                k = 0 
                while k < j:
                      if seq[k] <= ack[i]-1 and ack[i]-1 <= seq[k]+data_len[k]:
                         rtt.append([acktime[i], acktime[i] - seqtime[k]])
                      k = k + 1

                i = i + 1

            print ofo

        def start(self):
            print '###'
            print 'start case: SUM :)'
            sheet = self.xlsx.add_worksheet('sum')
            sheet.set_column(0, 0, 45) #set A column's width to 40
            sheet.write('A1', 'stream')
            sheet.write('B1', 'data len')
            sheet.write('C1', 'time')
            sheet.write('D1', 'synrtt')
            sheet.write('E1', 'TTFB')
            sheet.write('F1', 'retransmit')
            sheet.write('G1', 'ofo')
            sheet.write('H1', 'lost')
            #
            #sheet.write('I1', 'ishttp')
            #sheet.write('I1', 'isKeepLive')
            #sheet.write('J1', 'url')

            for id in self.streams:
                seq = [self.streams[id]['s_packets'][i]['seq']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['s_packets']))]
                ack = [self.streams[id]['c_packets'][i]['ack']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['c_packets']))]
                data_len = [self.streams[id]['s_packets'][i]['data_len'] for i in range(0, len(self.streams[id]['s_packets']))]
                seqtime = [self.streams[id]['s_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['s_packets']))]
                acktime = [self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['c_packets']))]

                c_len = len(self.streams[id]['c_packets'])
                s_len = len(self.streams[id]['s_packets'])
                sheet.write('A2', self.streams[id]['c_des'])
                sheet.write('B2', self.streams[id]['s_data_len'])

                #time
                i = c_len - 1
                while i > 0: 
                    if self.streams[id]['c_packets'][i]['flags'] & dpkt.tcp.TH_FIN:
                       sheet.write('C2', self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'])
                       break
                    i -= 1
                #synrtt
                i = 0
                while i < c_len: 
                    if self.streams[id]['c_packets'][i]['flags'] & dpkt.tcp.TH_ACK:
                        sheet.write('D2', self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'])
                        break
                    i += 1
                #TTFB
                i = 0
                first_data_time = 0
                get_data_time = 0
                while i < s_len: 
                    if self.streams[id]['s_packets'][i]['data_len'] != 0:
                        first_data_time = self.streams[id]['s_packets'][i]['ts']
                        break
                    i += 1
                i = 0
                while i < c_len: 
                    if self.streams[id]['c_packets'][i]['flags'] & dpkt.tcp.TH_ACK:
                        get_data_time = self.streams[id]['c_packets'][i+1]['ts']
                        break
                    i += 1
                sheet.write('E2', first_data_time - get_data_time)
                #retransmit
                self.retransmit(self.streams[id])
    
            print 'finish case: SUM :)'
