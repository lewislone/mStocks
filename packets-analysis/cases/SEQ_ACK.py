#coding: UTF-8
import sys
import utils
sys.path.append('./lib/dpkt-1.7/')
import dpkt
sys.path.append('./lib/XlsxWriter-0.7.3/')
import xlsxwriter


class SEQ_ACK:
        def __init__(self, streams_info, xlsx):
            '''SEQ_ACK init...
            '''
            self.xlsx = xlsx
            self.streams = streams_info
            self.timeformat = self.xlsx.add_format()
            self.timeformat.set_num_format('0.00000000')
            self.titleformat = self.xlsx.add_format({'bold': True, 'font_color': 'blue'})

        def data_inflight(self, seq, seqtime, ack, acktime, datalen):
            '''outstanding bytes'''
            i = 0
            send = 0
            acked = 0
            flight = []
            while i < len(seq):
                if send < seq[i] + datalen[i]:
                    send = seq[i] + datalen[i] 

                j = 0 
                while j < len(acktime):
                    if acktime[j] > seqtime[i]:
                        break
                    j = j + 1
            
                if j != 0:
                    j = j - 1
                if acked < ack[j]:
                    acked = ack[j]

                flight.append(send - acked) 
                i = i + 1 

            return flight

        def inster_chart(self, sheet, x, y, pos, des, yName):
            chart = self.xlsx.add_chart({'type': 'scatter'})
            chart.add_series({
                    'name':       yName,
                    'categories': x,
                    'values':     y,
                    'scatter':    {'type': 'star', 'color': 'red', 'size': 2}
            })
            chart.set_title({
                    'name': des,
                    'name_font': {
                        'name': 'Calibri',
                        'color': 'blue',
                        'size': 10 
                    },
            })
            #chart.set_size({'width': 720, 'height': 576})
            sheet.insert_chart(pos, chart)

        def start(self):
            print '###'
            print 'start case: SEQ_ACK :)'
            sheet = self.xlsx.add_worksheet('seq_ack')

            index = 2 
            for id in self.streams:
                if self.streams[id]['s_port'] == 30000 and self.streams[id]['c_port'] == 28288:#encrypt stream by ws
                    continue
                if len(self.streams[id]['c_packets']) == 0 or len(self.streams[id]['s_packets']) == 0:
                    continue
                if len(self.streams[id]['s_packets']) <= 5:
                    continue
                seq = [self.streams[id]['s_packets'][i]['seq']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['s_packets']))]
                ack = [self.streams[id]['c_packets'][i]['ack']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['c_packets']))]
                win = [self.streams[id]['c_packets'][i]['win'] for i in range(0, len(self.streams[id]['c_packets']))]
                seqtime = [self.streams[id]['s_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['s_packets']))]
                acktime = [self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['c_packets']))]
                data_len = [self.streams[id]['s_packets'][i]['data_len'] for i in range(0, len(self.streams[id]['s_packets']))]
                flight = self.data_inflight(seq, seqtime, ack, acktime, data_len) 
                ack[0] = 0
                sheet.write('A'+str(index-1), self.streams[id]['s_des'], self.titleformat)
                sheet.write('A'+str(index), 'seqtime')
                sheet.write('A'+str(index+1), 'seq')
                sheet.write('A'+str(index+2), 'inflight')
                sheet.write('A'+str(index+3), 'acktime')
                sheet.write('A'+str(index+4), 'ack')
                sheet.write('A'+str(index+5), 'win')
                sheet.write_row('B'+str(index), seqtime, self.timeformat)
                sheet.write_row('B'+str(index+1), seq)
                sheet.write_row('B'+str(index+2), flight)
                sheet.write_row('B'+str(index+3), acktime, self.timeformat)
                sheet.write_row('B'+str(index+4), ack)
                sheet.write_row('B'+str(index+5), win)

                if len(seq) <= 20:
                    index += 8
                    continue

                #chart SEQ
                self.inster_chart(sheet, '=seq_ack!$B$%d:$%s$%d'%(index, utils.nu2abc(len(seqtime)), index), \
                                        '=seq_ack!$B$%d:$%s$%d'%(index+1, utils.nu2abc(len(seq)), index+1), \
                                        'B%d'%(index+6), self.streams[id]['s_des'], 'seq')
                #chart ACk 
                self.inster_chart(sheet, '=seq_ack!$B$%d:$%s$%d'%(index+3, utils.nu2abc(len(acktime)), index+3), \
                                        '=seq_ack!$B$%d:$%s$%d'%(index+4, utils.nu2abc(len(ack)), index+4), \
                                        'J%d'%(index+6), self.streams[id]['c_des'], 'ack')
                #chart receive WIN 
                self.inster_chart(sheet, '=seq_ack!$B$%d:$%s$%d'%(index, utils.nu2abc(len(acktime)), index), \
                                        '=seq_ack!$B$%d:$%s$%d'%(index+5, utils.nu2abc(len(win)), index+5), \
                                        'B%d'%(index+22), self.streams[id]['c_des'], 'win')
                #chart data in flight 
                self.inster_chart(sheet, '=seq_ack!$B$%d:$%s$%d'%(index, utils.nu2abc(len(seqtime)), index), \
                                        '=seq_ack!$B$%d:$%s$%d'%(index+2, utils.nu2abc(len(flight)), index+2), \
                                        'J%d'%(index+22), self.streams[id]['s_des'], 'inflight')

                index += 39 
            print 'finish case: SEQ_ACK :)'

           # ##sent/ack 
           # grid(True)
           # ylabel('seqno', fontdict={'fontsize':20})
           # xlabel('time(s)', fontdict={'fontsize':20})
           # plot(seqtime, seq, 'ro:', linewidth=2, label='sent ')
           # plot(acktime, ack, 'go:', linewidth=2, label='acked ')
           # legend(title=self.filename, loc='best')
           # savefig('ack_timestamp.png', dpi=2000)
           # show()
