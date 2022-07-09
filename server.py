#!/usr/bin/env python3

import socket

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 1234))
    s.listen(5)
    return s

def handle_connection(sock):
    buf = sock.recv(1024)
    while len(buf) != 0:
        print(f'received {len(buf)} bytes')
        print(buf)
        buf = sock.recv(1024)
    print('connection closed')

def main():
    s = create_socket()
    print('socket created:', s)
    print('listening...')
    while True:
        (clientsocket, addr) = s.accept()
        print('connection accepted:', addr)
        handle_connection(clientsocket)

if __name__ == '__main__':
    main()
