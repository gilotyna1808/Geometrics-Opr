import socket
from geometrics_frame import GEOMETRICS_TASK
from time import sleep

SERVER_ADDRESS = ('localhost', 65432)
SOCKET_LISTENER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCKET_LISTENER.bind(SERVER_ADDRESS)

def send_task():
    pass

def task_listener():
    while True:
        data, address = SOCKET_LISTENER.recvfrom(4096)
        data = data.decode("utf-8")
        res = GEOMETRICS_TASK.get(data)
        print(res)
        msg = "".join(str(hex(x))[2:]+"-" for x in res)
        SOCKET_LISTENER.sendto(msg.encode("utf-8"),address)

task_listener()