# ex7.Syn Flood attack research.
# examine pcap file and look for the suspicious addresses that might attack the server and write them into a file.
# Author: Raz abergel.

"""THE ALGORITHM:
***  I used 4 factors in order to detect suspicious addresses  ***
all of these factors based on the idea that the attacker
want to sent lots of syn packets in a short time without responding to the
syn-ack packets that the server will send him back.
I want to track every activity that will be suspicious with the following factors:
1.Count the syn requests of every ip address
2.Count the ack requests of every ip address,if the ip has syn packets and has no ack packets at all,it is suspicious.
3.Determine a specific threshold that every ip that passed the limit will be suspicious.
4.calc the rate of sending ack packets per seconds --
 -- (using the time of the first packet and the last packet),if the rate is too high it is suspicious.
(I determent that above 5 packets per second is too high)"""

from collections import defaultdict
from scapy.layers.inet import TCP, IP
from scapy.utils import rdpcap

# Set the threshold for the number of SYN packets received from a single IP
THRESHOLD = 9

# Set the threshold for the rate at which SYN packets are received (in packets per second)
RATE_THRESHOLD = 5


def main():
    # Create dictionaries to track the number of SYN and ACK packets received from each IP
    syn_counter = defaultdict(int)
    ack_counter = defaultdict(int)

    # Read the pcap file and iterate over the packets
    packets = rdpcap(r'/synFloodTcpResearch\SYNflood.pcapng')

    start_time = packets[0].time  # store the time of the first packet as the start time
    end_time = packets[-1].time  # store the time of the last packet as the end time

    for packet in packets:
        # Check if the packet is a SYN packet
        if TCP in packet and packet[TCP].flags == 'S':
            # Increment the SYN counter for this IP address
            syn_counter[packet[IP].src] += 1
        # Check if the packet is an ACK packet
        elif TCP in packet and packet[TCP].flags == 'A':
            # Increment the ACK counter for this IP address
            ack_counter[packet[IP].src] += 1

    # Calculate the elapsed time of the attack
    elapsed_time = end_time - start_time

    # Open a file for writing
    with open('SuspiciousIpList.txt', 'w') as f:
        # Iterate over the dictionaries and check for mismatches between SYN and ACK counts
        for ip, syn_counter in syn_counter.items():
            # Calculate the rate at which SYN packets were received from this IP
            rate = syn_counter / elapsed_time
            if ip.startswith("100.64"):  # by doing a little research in wireshark we can identify that
                # the network start with '100.64' is apparently the target network and that is why we don't want
                # to add this group of ip addresses to the list.
                continue
            # if the syn counter is above the limit and on the top of that
            # this address didn't return any ack to the server.
            if syn_counter > THRESHOLD and ack_counter[ip] == 0:
                f.write(f'{ip}\n')
                continue
            # still suspicious about address that has more syn then ack
            if ack_counter[ip] != 0 and syn_counter > ack_counter[ip]:
                f.write(f'{ip}\n')
                continue
            # Check if the rate exceeds the threshold
            if rate > RATE_THRESHOLD:
                f.write(f'{ip}\n')


if __name__ == "__main__":
    # Call the main handler function
    main()
