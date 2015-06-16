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
        ###                                           'data_len': ,
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
        ###                                           'data_len': ,
        ###                                           'win': }, {},{},... ,{...}],
        ###                            'data_len':,
        ###                            'statt_time':,
        ###                            'end_time':},
        ###                'id_2':   {...},
        ###                       ...,
        ###                'id_x':   {...}}
        ###
            self.streams = streams_info
            self.xlsx = xlsx
             
        def start(self):
            '''the real work done here, analyse streams info and output the result into xlsx'''
            for stream in self.streams: #traverse all streams
                print '####### one stream ###########'
                print stream['s_des'] #like this: 'serverip:port -> clientip:port'
                print stream['c_des'] #like this: 'clientip:port -> serverip:port'
                print stream['c_ip'] #client ip of this stream
                print stream['s_ip'] #sverver ip of this stream
                print stream['c_port'] #client port of this stream 
                print stream['s_port'] #sverver port of this stream 
                print stream['data_len'] #size of data(server sent to client) 
                print stream['start_time'] #the time of this stream start 
                print stream['c_packets'] # a array save packet info from client to server of this stream
                print stream['s_packets'] # a array save packet info from server to client of this stream

                i = 0
                while i < len(stream['c_packets']): #traverse packets from clinet to server
                    print stream['c_packets'][i]['ts'] #time stamp of this packet
                    print stream['c_packets'][i]['src'] #src ip
                    print stream['c_packets'][i]['dst'] #dst ip
                    print stream['c_packets'][i]['dport'] #dst port
                    print stream['c_packets'][i]['sport'] #src port
                    print stream['c_packets'][i]['flags'] #syn|ack|fin|rst|push|urg|
                    print stream['c_packets'][i]['ack'] #ack number
                    print stream['c_packets'][i]['seq'] #seq number
                    print stream['c_packets'][i]['win'] #receive windown number
                    print stream['c_packets'][i]['data_len'] #size of this packet payload
                    i = i + 1

                i = 0
                while i < len(stream['c_packets']): #traverse packets from server to client
                    print stream['s_packets'][i]['ts'] #time stamp of this packet
                    print stream['s_packets'][i]['src'] #src ip
                    print stream['s_packets'][i]['dst'] #dst ip
                    print stream['s_packets'][i]['dport'] #dst port
                    print stream['s_packets'][i]['sport'] #src port
                    print stream['s_packets'][i]['flags'] #syn|ack|fin|rst|push|urg|
                    print stream['s_packets'][i]['ack'] #ack number
                    print stream['s_packets'][i]['seq'] #seq number
                    print stream['s_packets'][i]['win'] #receive windown number
                    print stream['s_packets'][i]['data_len'] #size of this packet payload
                    i = i + 1
