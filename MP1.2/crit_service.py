from scapy.all import IP
import time
import random
import socket
import sys
from checkpoint import save_state

source_ip = ["192.168.21.10", "124.82.31.1", "192.168.1.1", "127.53.1.178", "168.1.127.20", "167.54.133.2"]
destination_ip = ["192.168.82.1", "186.123.54.2", "178.65.111.3"]
blacklisted_ips = ["192.168.1.1", "158.123.37.1", "167.54.133.2"]

def create_packet():
    src_ip = random.choice(source_ip)
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

state = {"processed": 0, "blocked": 0, "blacklisted_ips": blacklisted_ips}
save_state(state)

monitor_ip = "127.0.0.1"
monitor_port = 9999
client_port = 10000
heartbeat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("127.0.0.1", client_port))
client_socket.settimeout(0.2)

print("Security service started", flush=True)

while True:
    packet = create_packet()
    message = check_packet(packet)
    print(message, flush=True)

    state["processed"] += 1
    if message.startswith("blocked:"):
        state["blocked"] += 1
    save_state(state)

    try:
        data, address = client_socket.recvfrom(1024)
        request = data.decode().strip()
        if request == "STATUS":
            response = f"PRIMARY processed={state['processed']} blocked={state['blocked']}"
        elif request.startswith("CHECK "):
            address_to_check = request[6:].strip()
            if address_to_check in state["blacklisted_ips"]:
                response = "blocked: " + address_to_check
                state["blocked"] += 1
            else:
                response = "accepted: " + address_to_check
            state["processed"] += 1
            save_state(state)
        else:
            response = "Use STATUS or CHECK <ip>"
        client_socket.sendto(response.encode(), address)
    except socket.timeout:
        pass

    heartbeat_socket.sendto(b"HEARTBEAT", (monitor_ip, monitor_port))
    print("Heartbeat sent", flush=True)
    time.sleep(1)

    #10% chance for crash
    if random.random() < 0.10:
        print("Service crashed!", flush=True)
        heartbeat_socket.close()
        client_socket.close()
        sys.exit(1)
