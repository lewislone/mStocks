#coding: UTF-8
import os
import re
from matplotlib.pyplot import *

def search_stream(streams, sk):
    for stream in streams:
        if stream['sk'] == sk:
           return stream

    return False 

def find_item(source, item_name, default):
    filter = item_name+':(\d*) '
    value = re.findall(filter, source, re.S)
    if len(value) > 0:
        return value[0]
    else:
        return default

def parse_file(f):
        set = 1 
        sp = '/'
        one_case = 0 
        streams = []
        line = f.readline()
        while line:
            ##one set
            if len(line) == 27:#time: 2015-03-02 15:29.438286145
                time = line
            
                line = f.readline()
                if len(line) == 27:#time: 2015-03-02 15:29.438286145
                    one_case = 0
                    for stream in streams:
                         stream['cwnd'].append("0")
                         stream['ssthresh'].append("0")
                         stream['rtt'].append("0")
                         stream['ca_state'].append("0")
                    continue

                while line and len(line) != 27:
                    new = 0 
                    one_case = one_case + 1
                    if one_case == 1:#sk: ino:2389445 sk:276a8180ffff8804
                        '''ID'''
                        value = line.split()
                        if len(value) == 8:
                            (rq, sq, src, dst, timer, user, ino, sk) = value 
                        if len(value) == 7:
                            (rq, sq, src, dst, timer, ino, sk) = value 
                        stream = search_stream(streams, sk[3:])
                        if stream is False:
                            stream = {}
                            stream['src'] = src 
                            stream['dst'] = dst 
                            stream['sk'] = sk[3:]
                            stream['cwnd'] = []
                            stream['ssthresh'] = []
                            stream['ca_state'] = []
                            stream['rtt'] = []
                            stream['reordering'] = []
                            new = 1
                       
                    elif one_case == 2: 
	                #mem:(r0,w505060,f68380,t0) sack bic wscale:9,9 rto:675 rtt:439/30 ato:40 mss:1460 cwnd:148 ca_state:0 send 3.9Mbps unacked:126 rcv_space:14600
                        '''CNWD'''
                        nline = line[1 : line.index('@')+8]
                        value = nline.split()
                        one_case = 0
                        if len(value) == 11:
                            stream['reordering'].append(find_item(line, 'reordering', 3))
                            (mem, sack, alg, wscale, rto, rtt, ato, mss, cwnd, ssthresh, ca_state) = value 
                            stream['cwnd'].append(cwnd[5:])
                            stream['ssthresh'].append(ssthresh[9:])
                            stream['ca_state'].append(ca_state[9:])
                            stream['rtt'].append(rtt[rtt.index(sp)+1:])
                        elif len(value) == 10:
                            stream['reordering'].append(find_item(line, 'reordering', 3))
                            (mem, sack, alg, wscale, rto, rtt, ato, mss, cwnd, ca_state) = value 
                            if cwnd[0:4] == "cwnd":
                                stream['cwnd'].append(cwnd[5:])
                                stream['ssthresh'].append("0")
                                stream['ca_state'].append(ca_state[9:])
                                stream['rtt'].append(rtt[rtt.index(sp)+1:])
                            else:
                                stream['cwnd'].append("0")
                                stream['ssthresh'].append(cwnd[9:])
                                stream['ca_state'].append(ca_state[9:])
                                stream['rtt'].append(rtt[rtt.index(sp)+1:])
                        else:
                            print 'len of value : '+ str(len(value))
                            line = f.readline()
                            continue
                    if new == 1:
                        streams.append(stream)
                    line = f.readline()

        f.close()
        return streams

if __name__ == '__main__':

    cap_file = sys.argv[1]
    if not os.path.exists(cap_file):
        print cap_file + " not exist"
        exit() 

    f = file(cap_file)
    streams = parse_file(f)
    print len(streams)
    stream = {}
    for stream in streams:
        cwnd = [int(cwnd) for cwnd in stream['cwnd']]
        ssthresh = [int(ssthresh) for ssthresh in stream['ssthresh']]
        rtt = [float(rtt) for rtt in stream['rtt']]
        ca_state = [int(ca_state) for ca_state in stream['ca_state']]
        reordering = [int(reordering) for reordering in stream['reordering']]
        print stream['sk'] 

        ##cwnd 
        grid(True)
        ylabel('cwnd', fontdict={'fontsize':20})
        xlabel('time(s)', fontdict={'fontsize':20})
        plot(range(len(cwnd)), ssthresh, 'go:', linewidth=2, label='ssh')
        plot(range(len(cwnd)), cwnd, 'ro:', linewidth=2, label='cwnd')
        #plot(range(len(rtt)), rtt, 'yo:', linewidth=2, label='rtt')
        plot(range(len(ca_state)), ca_state, 'bo:', linewidth=2, label='ca_state')
        plot(range(len(reordering)), reordering, 'co:', linewidth=2, label='reordering')
        legend(title=cap_file + "(cwnd)", loc='best')
        #savefig('ack_timestamp.png')
        show()
