from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from pynput.keyboard import Controller, Key
import json
import sys

# Set up server listen for input instructions
PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )

msg_socket = socket( AF_INET, SOCK_DGRAM )
msg_socket.bind( (hostName, PORT_NUMBER) )

# keyboard controller
keyboard = Controller()
print("Test server listening on port {0}\n".format(PORT_NUMBER))

def get_key_enum(key):
    key_name = key.split('.')[1]
    return getattr(Key, key_name)

while True:
    (data,addr) = msg_socket.recvfrom(SIZE)
    data = data.decode('utf-8')
    # data is in form: {key} {type}
    # e.g. 'a' pressed
    res = data.split(' ')
    print(res)
    if res[1] == 'released':
        try:
            keyboard.release(res[0])
        except ValueError:
            key_obj = get_key_enum(res[0])
            keyboard.release(key_obj)

    elif res[1] == 'pressed':
        try:
            keyboard.press(res[0])
        except ValueError:
            key_obj = get_key_enum(res[0])
            keyboard.press(key_obj)

sys.exit()
