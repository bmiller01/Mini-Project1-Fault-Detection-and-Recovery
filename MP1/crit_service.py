from scapy.all import IP
import time
import random
import socket
import sys
from datetime import datetime, timezone


source_ip = ["192.168.21.10", "124.82.31.1", "192.168.1.1", "127.53.1.178", "168.1.127.20", "167.54.133.2"]
destination_ip =["192.168.82.1", "186.123.54.2", "178.65.111.3"]
blacklisted_ips = ["192.168.1.1", "158.123.37.1", "167.54.133.2"]

def create_packet():
    src_ip =random.choice(source_ip)
    dst_ip = random.choice(destination_ip)
    packet = IP(src=src_ip, dst=dst_ip)
    return packet

def check_packet(packet):
    source = packet[IP].src
    if source in blacklisted_ips:
        message = f"blocked: {source}"
    else:
        message = f"accepted: {source}"
    return message

monitor_ip = "127.0.0.1"
monitor_port = 9999
heartbeat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Security service started", flush=True)

while True:
    packet = create_packet()
    print(check_packet(packet),flush=True)

    heartbeat_socket.sendto(b"HEARTBEAT", (monitor_ip, monitor_port))
    print("Heartbeat sent", flush=True)

    time.sleep(1)

    #10% chance to crash 
    if random.random() < 0.10:
        print("Service crashed!", flush= True)
        heartbeat_socket.close()
        sys.exit(1)
