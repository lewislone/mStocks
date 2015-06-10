#coding: UTF-8
import sys
sys.path.append('./lib/dpkt-1.7/')
import dpkt
sys.path.append('./lib/XlsxWriter-0.7.3/')
import xlsxwriter


class seqAck:
        def __init__(self, streams_info, xlsx):
            '''SEQ_ACK init...
            '''
            print 'init case: SEQ_ACK :)'
            self.xlsx = xlsx
            self.streams = streams_info
            self.timeformat = self.xlsx.add_format()
            self.timeformat.set_num_format('0.00000000')

        def start(self):
            print 'start case: SEQ_ACK :)'
            sheet = self.xlsx.add_worksheet('seq_ack')

            for id in self.streams:
                print self.streams[id]['s_packets'][0]['flags'] & dpkt.tcp.TH_SYN
                print self.streams[id]['c_packets'][0]['flags'] & dpkt.tcp.TH_SYN
                print self.streams[id]['c_packets'][1]['flags'] & dpkt.tcp.TH_SYN
                seq = [self.streams[id]['s_packets'][i]['seq']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['s_packets']))]
                ack = [self.streams[id]['c_packets'][i]['ack']-self.streams[id]['s_packets'][0]['seq'] for i in range(0, len(self.streams[id]['c_packets']))]
                seqtime = [self.streams[id]['s_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['s_packets']))]
                acktime = [self.streams[id]['c_packets'][i]['ts']-self.streams[id]['start_time'] for i in range(0, len(self.streams[id]['c_packets']))]
                ack[0] = 0
                sheet.write('A1', 'seqtime')
                sheet.write('A2', 'seq')
                sheet.write('A1', 'acktime')
                sheet.write('A2', 'ack')
                sheet.write_row('B1', seqtime, self.timeformat)
                sheet.write_row('B2', seq)
                sheet.write_row('B3', acktime, self.timeformat)
                sheet.write_row('B4', ack)

            #chart
            chart = self.xlsx.add_chart({'type': 'scatter'})
            chart.add_series({
                    'categories': '=seq_ack!$B$3:$HXS$3',
                    'values':     '=seq_ack!$B$4:$HXS$4',
                    'scatter':    {'type': 'plus', 'color': 'blue', 'size': 2}
            })
            chart.add_series({
                    'categories': '=seq_ack!$B$1:$QVS$1',
                    'values':     '=seq_ack!$B$2:$QVS$2',
                    'scatter':    {'type': 'star', 'color': 'red', 'size': 2}
            })
            #chart.set_size({'width': 720, 'height': 576})
            sheet.insert_chart('D6', chart)
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
