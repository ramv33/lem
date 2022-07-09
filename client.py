#!/usr/bin/env python3

import os
import sys
import socket
import hashlib

BUFFSIZE = 4096

def connect_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

    m = hashlib.sha256()
    m.update(buf)
    return m.hexdigest()

def send_file(sock, file):
    if not os.path.isfile(file):
        print(f'{file} is not a file')
        return

    f = open(file, 'rb')
    print(f'sending file {file}')
    digest = hashlib.sha256()
    buf = f.read(BUFFSIZE)
    while len(buf) != 0:
        digest.update(buf)
        print(f'sent {sock.send(buf)} bytes')
        buf = f.read(BUFFSIZE)
    print(f'hash: {digest.hexdigest()}')

def main():
    if len(sys.argv) < 4:
        print(f'usage: {sys.argv[0]} ip port file')
        exit(1)

    s = connect_server(sys.argv[1], int(sys.argv[2]))
    send_file(s, sys.argv[3])
    s.close()

if __name__ == '__main__':
    main()
