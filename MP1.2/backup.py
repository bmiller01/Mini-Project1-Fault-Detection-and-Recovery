import socket
import time
from checkpoint import load_state, save_state

#monitor starts this prgram after the primary stops getting areponse
try:
    state = load_state()
except (OSError, ValueError):
    print("Backup cannot start: checkpoint missing or damaged", flush=True)
    raise SystemExit(1)

monitor_ip = "127.0.0.1"
monitor_port = 9999
client_port = 10000

heartbeat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("127.0.0.1", client_port))
client_socket.settimeout(0.2)

print("Backup started with saved state:", state, flush=True)

while True:
    try:
        data, address = client_socket.recvfrom(1024)
        request = data.decode().strip()
        if request == "STATUS":
            response = f"BACKUP processed={state['processed']} blocked={state['blocked']}"
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
    time.sleep(1)
