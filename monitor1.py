import socket
import time
from datetime import datetime
host = "127.0.0.1"
port = 9999
timeout = 3

monitor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
monitor.bind((host, port))
monitor.settimeout(1)

print("Monitor started, waiting for heartbeats...")

last_heartbeat = None
service_down = False

while True:
    try:
        data, address = monitor.recvfrom(1024)
        if data.decode() == "HEARTBEAT":
            last_heartbeat = time.time()
            service_down = False
            print("Heartbeat received at", datetime.now())

    except socket.timeout:
        pass

    if last_heartbeat is not None:
        if time.time() - last_heartbeat >= timeout and not service_down:
            message = "Service is down! No heartbeat received."
            print(datetime.now(), message)

            # Save failure to log file
            with open("incidents.log", "a") as file:
                file.write(str(datetime.now()) + " " + message + "\n")

            service_down = True
