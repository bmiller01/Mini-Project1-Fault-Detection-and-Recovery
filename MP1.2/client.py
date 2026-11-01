import socket
import time
#nothinmg crazy for client should just need to show before andd after but feel free toe dit however yall see fit
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(2)

while True:
    try:
        client.sendto(b"STATUS", ("127.0.0.1", 10000))
        data, address = client.recvfrom(1024)
        print(data.decode(), flush=True)
    except socket.timeout:
        print("No response (service may be switching)", flush=True)
    time.sleep(1)
