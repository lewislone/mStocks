#!/bin/sh

> 91-tos-cwnd
while [ 1 ]; do
        date '+%F %H:%M.%N' >> 91-tos-cwnd
        ss -imtoep state established 'sport = :12356' | grep -v Recv-Q >> 91-tos-cwnd
        usleep 10
done

