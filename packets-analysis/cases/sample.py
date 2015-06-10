#coding: UTF-8
import sys
sys.path.append('./lib/XlsxWriter-0.7.3/')
import xlsxwriter

###note: class name must the same with name of this file 
class sample:

        def __init__(self, streams_info, xlsx):
            '''do some init'''
        ###note: there are two input parameters  
        ###     xlsx: return by xlsxwriter.Workbook(filename)
        ###     streams_info: streams info get from stream.py
        ###       streams= {
        ###                 'id_1':  {
        ###                            'c_ip':
        ###                            's_ip':
        ###                            'c_port':
        ###                            's_port':
        ###                            'c_des':,
        ###                            'c_packets':[{
        ###                                           'ts': , 
        ###                                           'id': , 
        ###                                           'src': , 
        ###                                           'dst': , 
        ###                                           'sport': ,
        ###                                           'dport': ,
        ###                                           'flags': ,
        ###                                           'seq': ,
        ###                                           'ack': ,
        ###                                           'win': }, {},{},... ,{...}],
        ###                            's_des':,
        ###                           's_packets':[{
        ###                                           'ts': , 
        ###                                           'id': , 
        ###                                           'src': , 
        ###                                           'dst': , 
        ###                                           'sport': ,
        ###                                           'dport': ,
        ###                                           'flags': ,
        ###                                           'seq': ,
        ###                                           'ack': ,
        ###                                           'win': }, {},{},... ,{...}],
        ###                            'data_len':,
        ###                            'statt_time':,
        ###                            'end_time':},
        ###                'id_2':   {...},
        ###                       ...,
        ###                'id_x':   {...}}
        ###
             
        def start(self):
            '''the real work done here, analyse streams info and output the result into xlsx'''
