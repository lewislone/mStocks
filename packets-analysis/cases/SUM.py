#coding: UTF-8
import sys
sys.path.append('./lib/XlsxWriter-0.7.3/')
import xlsxwriter

class SUM:
        def __init__(self, streams_info, xlsx):
            self.xlsx = xlsx
            self.streams = streams_info

        def start(self):
            print '###'
            print 'start case: SUM :)'
            sheet = self.xlsx.add_worksheet('sum')
            sheet.set_column(0, 0, 45) #set A column's width to 40
            sheet.write('A1', 'stream')
            sheet.write('B1', 'data len')
            sheet.write('C1', 'time')
            sheet.write('D1', 'rtt')
            sheet.write('E1', 'lost')
            sheet.write('F1', 'retransmit')
            sheet.write('G1', 'ofo')
            sheet.write('H1', 'TTFB')
            #
            #sheet.write('I1', 'isKeepLive')
            #sheet.write('I1', 'ishttp')
            #sheet.write('J1', 'url')

            for id in self.streams:
                sheet.write('A2', self.streams[id]['s_des'])
                sheet.write('B2', self.streams[id]['data_len'])
                
    
            print 'finish case: SUM :)'
