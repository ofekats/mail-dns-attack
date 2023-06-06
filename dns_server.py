from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import UDP
from scapy.layers.dns import DNS
from scapy.layers.dns import DNSRR

def dns_server(packet):
    print(packet[DNS].qd.qname)
    if DNS in packet and packet[DNS].opcode == 0 and packet[DNS].qd.qname == b'example.com.':  # Check if DNS layer exists and it's a query
        print("Received DNS Query:")
        print("Source IP:", packet[IP].src)
        print("Destination IP:", packet[IP].dst)
        print("Domain Name:", packet[DNS].qd.qname.decode())

        print(packet.show())

# Sniff DNS traffic and invoke dns_server for each received packet
sniff(filter="udp port 53", prn=dns_server)