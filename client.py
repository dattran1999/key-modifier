#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname_ex, gethostname
from pynput.keyboard import Key, Listener

# Find the local IP address
# https://stackoverflow.com/a/1267524
SERVER_IP   = [l for l in ([ip for ip in gethostbyname_ex(gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket(AF_INET, SOCK_DGRAM)]][0][1]]) if l][0][0]
PORT_NUMBER = 5000

SERVER = (SERVER_IP, PORT_NUMBER)
SIZE = 1024
print ("Client sending packets to {0}:{1}\n".format(SERVER_IP, PORT_NUMBER))

msg_socket = socket( AF_INET, SOCK_DGRAM )

def on_press(key):
    msg = None
    try:
        msg = '{0} pressed'.format(key.char)
    except:
        msg = '{0} pressed'.format(key)
    print(msg)
    msg_socket.sendto(msg.encode('utf-8'), SERVER)

def on_release(key):
    msg = None
    try:
        msg = '{0} released'.format(key.char)
    except:
        msg = '{0} released'.format(key)
    print(msg)
    msg_socket.sendto(msg.encode('utf-8'), SERVER)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

