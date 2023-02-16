from scapy.all import *

p = IP(dst="8.8.8.8")/ICMP()/Raw(load="yes my leigh")
r = sr1(p)
print(r.show())