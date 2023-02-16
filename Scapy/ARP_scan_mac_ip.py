from scapy.all import *
from scapy.layers.l2 import Ether, ARP


def scan(ip):
    arp_req = ARP(pdst = ip) #Ether(dst = 'ff:ff:ff:ff:ff:ff')/
    try:
        answer = sr1(arp_req,verbose = 0,timeout=1,retry = 1)
        return "the mac adderss of " + ip +" is:  "+  answer[ARP].hwdst
    except Exception as e:
        return ip + "- mac not available. the address is free to use"


def main():
    list_mac = []
    for curr in range(255):
       print(scan(f'10.0.0.{curr}'))





if __name__ == "__main__":
    # Call the main handler function
    main()

### important!
#packets without the second layer supposed to be sent with "send"
#and packets with the second layer supposed to be sent with "sendp"

# from scapy.all import *
#
# p1 = Ether()/IP(dst='8.8.8.8')/Raw("abc")
# send(p1)
# print('***')
# p2 = Ether()/IP(dst='8.8.8.8')/Raw("def")
# sendp(p2)
# print('***')
# p3 = IP(dst='8.8.8.8')/Raw("ghi")
# send(p3)
# print('***')
# p4 = IP(dst='8.8.8.8')/Raw("jkl")
# sendp(p4)


# for i in range(254):
# destination = NETWORK_ID + str(i)
# p = ARP (pdst=destination)
# try:
# sr1(p, verbose=0, timeout=0.1)
# print(str(r[ARP].hwsrc), str(r[ARP].psrc))
# except:
# print(destination + not available")
