import socket
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path

host = "127.0.0.1"
port = 9999
timeout = 3

monitor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
monitor.bind((host, port))
monitor.settimeout(1)

print("Monitor started, waiting for heartbeats...", flush=True)

last_heartbeat = None
service_down = False
backup_started = False
backup_process = None

def log_message(message):
    print(datetime.now(), message, flush=True)
    with open("incidents.log", "a") as file:
        file.write(str(datetime.now()) + " " + message + "\n")

try:
    while True:
        try:
            data, address = monitor.recvfrom(1024)
            if data.decode() == "HEARTBEAT":
                last_heartbeat = time.time()
                print("Heartbeat received at", datetime.now(), flush=True)

                if backup_started and service_down:
                    log_message("[Service Restored] Backup is sending heartbeats")
                    service_down = False

        except socket.timeout:
            pass

        if last_heartbeat is not None:
            if time.time() - last_heartbeat >= timeout and not service_down:
                log_message("[Crash Detected] No heartbeat received")
                service_down = True

                if not backup_started:
                    log_message("[Failover Triggered] Starting backup service")
                    backup_path = Path(__file__).with_name("backup.py")
                    backup_process = subprocess.Popen([sys.executable, str(backup_path)])
                    backup_started = True
finally:
    monitor.close()
