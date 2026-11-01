import socket
import time
from pathlib import Path

#Atatck for MP1.2, corrupting saved checkponts crash
#to run start the monitor and crit service first, then this one.

checkpoint = Path(__file__).with_name("checkpoint.json")
server_ip = "127.0.0.1"
server_port = 10000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.5)

print("Waiting for the primary service to crash...")

#need service running befoire crash, It took me way to long to relaize that mistake lol
while True:
    try:
        client.sendto(b"STATUS", (server_ip, server_port))
        data, address = client.recvfrom(1024)
        if data.decode().startswith("PRIMARY"):
            print("Primary is running:", data.decode())
            break
    except socket.timeout:
        print("Waiting for primary...")
    time.sleep(1)

#whenever it stiop repsonding, damage the saved checkpoint.
while True:
    try:
        client.sendto(b"STATUS", (server_ip, server_port))
        data, address = client.recvfrom(1024)
        print("Service still responding:", data.decode())
    except socket.timeout:
        print("Primary stopped responding. Corrupting checkpoint...")
        if checkpoint.exists():
            with open(checkpoint, "w") as file:
                file.write("This is not valid JSON")
            print("Checkpoint corrupted:", checkpoint.name)
            print("Watch the monitor and backup terminals for the result.")
        else:
            print("Checkpoint file not found.")
        break
    time.sleep(0.2)

client.close()
