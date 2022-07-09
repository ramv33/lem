#!/usr/bin/env python3

import sys
import socket

def connect_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def main():
    if len(sys.argv) < 4:
        print(f'usage: {sys.argv[0]} ip port file')
        exit(1)

    s = connect_server(sys.argv[1], int(sys.argv[2]))
    f = open(sys.argv[3], 'rb')
    print(f'sending file {sys.argv[3]}')
    print(f'sent {s.send(f.read())} bytes')
    s.close()

if __name__ == '__main__':
    main()
