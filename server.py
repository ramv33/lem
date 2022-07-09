#!/usr/bin/env python3

import socket

BUFFSIZE = 4096

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 1234))
    s.listen(5)
    return s

def recvfile(sock, filename):
    f = open('question', 'wb')
    buf = sock.recv(BUFFSIZE)
    while len(buf) != 0:
        print(f'received {len(buf)} bytes')
        f.write(buf)
        #print(buf)
        buf = sock.recv(BUFFSIZE)
    print('connection closed')
    print(f'wrote file {filename}')

def listen():
    s = create_socket()
    filename = 'question'
    print('socket created:', s)
    print('listening')
    while True:
        (clientsocket, addr) = s.accept()
        print('connection accepted:', addr)
        recvfile(clientsocket, filename)

def main():
    listen()

if __name__ == '__main__':
    main()
