import socket
import time
import sys

monitor_ip = "127.0.0.1"
monitor_port = 9999

#create a socket between adversary's script and monitor
adversary_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#attack1: transmit fake heartbeat messages to the monitor
spoofs_sent = 0
while spoofs_sent < 3:
    adversary_socket.sendto(b"HEARTBEAT", (monitor_ip, monitor_port))
    print("Heartbeat sent from adversary")
    time.sleep(1)
    spoofs_sent += 1

adversary_socket.close()
sys.exit(1)
