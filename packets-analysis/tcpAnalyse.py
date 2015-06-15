#coding: UTF-8
import os, sys, os, stat
import traceback
import config
sys.path.append('./lib/XlsxWriter-0.7.3/')
import xlsxwriter

class ANALYSIS_TCP:
        def __init__(self, file_name, streams_info):
            '''analysis init...
            '''
            ##init excel env
            self.filename = file_name
            self.xlsx = xlsxwriter.Workbook(file_name + '.xlsx')
            self.streams = streams_info
            self.timeformat = self.xlsx.add_format()
            self.timeformat.set_num_format('0.00000000')

            ##load test cases
            path = './cases/'
            sys.path.append(path)
            for item in os.listdir(path):
                subpath = os.path.join(path, item)
                mode = os.stat(subpath)[stat.ST_MODE]
                if stat.S_ISDIR(mode):
                    sys.path.append(subpath)

        def start(self):
            for module in config.get_butlers_from_ini():
                try:
                   case = __import__(module)
                   obj = getattr(case, module)
                   handle = obj(self.streams, self.xlsx)
                   handle.start()

                except Exception as e:
                    if module:
                        #print e
                        print traceback.print_exc()
                        print 'load module: %s failed!!!!' % module
                    pass

        def save_work(self):
            self.xlsx.close()

