#coding: UTF-8
import os
import sys
import json
import parse
import tcpAnalyse

if __name__ == '__main__':
    cap_file = sys.argv[1]
    if not os.path.exists(cap_file):
        print cap_file + " not exist"
        exit()

    collect = parse.PCAP_PARSE()
    f = file(cap_file)
    #f = file("/home/lewis/work/tmp/xx.cap")
    collect.collect_streams(f)
    #print collect.stream.streams

    file = open(cap_file + 'stream.json', "ab")
    json.dump(collect.stream.streams, file)

    analysis = tcpAnalyse.ANALYSIS_TCP(cap_file, collect.stream.streams)
    analysis.start()
    analysis.save_work()


   # stream = {}
   # for stream in streams:
   #     time1 = [seq[0] for seq in stream['seq']]
   #     seq = [seq[1] for seq in stream['seq']]

   #     if len(seq) < 10:
   #         continue

   #     des1 = stream['src'] + ":" + str(stream['sport']) + " -> " + stream['dst'] + ":" + str(stream['dport'])
   #     des2 = stream['dst'] + ":" + str(stream['dport']) + " -> " + stream['src'] + ":" + str(stream['sport'])
   #     stream_id = hashlib.md5(des2).hexdigest()
   #     print stream['stream_id']
   #     stream = parse.search_stream(streams, stream_id)
   #     if stream == False:
   #         continue
   #     time2 = [ack[0] for ack in stream['ack']]
   #     ack = [ack[1] for ack in stream['ack']]
   #     win = [win[1] for win in stream['win']]

   #     ##remove zero value
   #     if seq[0] == 0:
   #         seq[0] = seq[1]
   #         time1[0] = time1[1]
   #     if ack[0] == 0:
   #         ack[0] = ack[1]
   #         time2[0] = time2[1]

   #     ##skip server(only send data) direction package
   #     if ack[1] == ack[len(ack)/2]:
   #         continue

   #     ##outstanding bytes
   #     i = 0
   #     send = 0
   #     acked = 0
   #     flight = []
   #     while i < len(seq):
   #         if send < seq[i]:
   #             send = seq[i] 

   #         j = 0 
   #         for time in time2:
   #             if time > time1[i]:
   #                break
   #             j = j + 1
   #         
   #         if j == len(time2):
   #             j = j - 1
   #         if acked < ack[j]:
   #             acked = ack[j]
   #         flight.append(send - acked) 
   #         i = i + 1 

   #    # ##sent/ack 
   #    # grid(True)
   #    # ylabel('seqno', fontdict={'fontsize':20})
   #    # xlabel('time(s)', fontdict={'fontsize':20})
   #    # plot(time1, seq, 'ro:', linewidth=2, label='sent ' + des1)
   #    # plot(time2, ack, 'go:', linewidth=2, label='acked ' + des2)
   #    # legend(title=cap_file, loc='best')
   #    # #savefig('ack_timestamp.png')
   #    # show()

   #    # ##receive windows
   #    # grid(True)
   #    # ylabel('windows', fontdict={'fontsize':20})
   #    # xlabel('time(s)', fontdict={'fontsize':20})
   #    # plot(time2, win, 'y-o', linewidth=2, label='win time(s) ' + des1)
   #    # legend(title=cap_file +'(windows)', loc='best')
   #    # #savefig('ack_timestamp.png')
   #    # show()

   #    # ##outstanding bytes
   #    # grid(True)
   #    # ylabel('outstanding', fontdict={'fontsize':20})
   #    # xlabel('time(s)', fontdict={'fontsize':20})
   #    # plot(time1, flight, 'y-o', linewidth=2, label='outstanding time(s) ' + des1)
   #    # legend(title=cap_file+ '(outstanding)', loc='best')
   #    # #savefig('ack_timestamp.png')
   #    # show()
