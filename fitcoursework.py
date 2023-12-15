# -*- coding: utf-8 -*-
"""FITCoursework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fpveVL59gGPDPeTr93K99PhtLlw3wAvm
"""
import subprocess
subprocess.run(["sudo", "ip", "-6", "route", "add", "default", "via", "inet6", "dev", "<interface_name>"])

import scapy
#!pip install scapy_http

#from scapy.all import *

#from google.colab import drive
#drive.mount('/content/drive')
from scapy.all import rdpcap
pcap_file_path = 'Data/link1_1-VPN/link1_Test11_34_54.pcap'

packets = rdpcap(pcap_file_path)

#!pip install scapy



pcap_file_path = 'Data/link1_1-VPN/link1_Test11_34_54.pcap'
packets = rdpcap(pcap_file_path)

# Display information about the first few packets
for i in range(min(5, len(packets))):
    print(f"Packet {i + 1}:\n{packets[i].summary()}\n")

# Additional information about the pcap file
print(f"Total number of packets: {len(packets)}")

#from scapy.all import rdpcap, IP, TCP, UDP
def is_vpn(packet):
    # Check if the packet contains specific characteristics associated with VPN traffic
    return (
        IP in packet and
        (
            (TCP in packet and (packet[TCP].dport == 1194 or packet[TCP].sport == 1194)) or
            (UDP in packet and (packet[UDP].dport == 500 or packet[UDP].sport == 500))
        )
    )

# Load the pcap file
pcap_file_path = '/content/drive/MyDrive/FIT/Data/link1_1-VPN/link1_Test11_37_33.pcap'
packets = rdpcap(pcap_file_path)

# Classify packets into VPN and non-VPN
vpn_packets = [packet for packet in packets if is_vpn(packet)]
non_vpn_packets = [packet for packet in packets if not is_vpn(packet)]

# Print basic statistics
print(f"Total packets: {len(packets)}")
print(f"VPN packets: {len(vpn_packets)}")
print(f"Non-VPN packets: {len(non_vpn_packets)}")

#from scapy.all import rdpcap
#import os

def detect_vpn_packets(pcap_file):
    # Common VPN ports (for demonstration purposes)
    common_vpn_ports = [1194, 1723, 500, 4500,443,1701]

    vpn_packet_count = 0
    total_packet_count = 0

    try:
        packets = rdpcap(pcap_file)

        for packet in packets:
            total_packet_count += 1

            # Check if the packet has a TCP or UDP layer
            if packet.haslayer('TCP'):
                tcp_layer = packet['TCP']
                if tcp_layer.sport in common_vpn_ports or tcp_layer.dport in common_vpn_ports:
                    vpn_packet_count += 1
            elif packet.haslayer('UDP'):
                udp_layer = packet['UDP']
                if udp_layer.sport in common_vpn_ports or udp_layer.dport in common_vpn_ports:
                    vpn_packet_count += 1

    except FileNotFoundError:
        print(f"File not found: {pcap_file}")
        return
    except Exception as e:
        print(f"An error occurred while processing {pcap_file}: {e}")
        return

    print(f"Total packets in {pcap_file}: {total_packet_count}, Suspected VPN packets: {vpn_packet_count}")


# Define the root folder path
root_folder_path = '/content/drive/MyDrive/FIT/Data/'

# Walk through each folder and subfolder in the directory
for folder_name, sub_folders, file_names in os.walk(root_folder_path):
    for filename in file_names:
        if filename.endswith(".pcap"):
            # Construct full file path
            file_path = os.path.join(folder_name, filename)
            detect_vpn_packets(file_path)

