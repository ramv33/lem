#!/usr/bin/env python3

import os
import sys
import time
import socket
from socket import gethostbyname
import hashlib
import argparse
import pandas as pd
import pymongo

from assign_qns import *
from getname import *
import myconstants

def printerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getips(iplist):
    f = open(iplist, 'r')
    iplst = [ip.strip() for ip in f.readlines()]
    return iplst

def connect_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

    m = hashlib.sha256()
    m.update(buf)
    return m.hexdigest()

'''
	logwrite writes a csv file with following fields
        0. system time
        1. ip/system: ip address/system name
        2. question_head: first line of question from question file
        3. question filename
        4. question file hash
'''
def logwrite(logfile, logdict, conn):
    dbname = myconstants.DBNAME
    collname = myconstants.COLLECTION_NAME
    try:
        qnfp = open(logdict['qpath'], 'r')
        log = {
            'Time': [time.strftime(myconstants.TIMEFMT)],
            # if system list was given as domain names, we need to do DNS lookup
            'Name': getname_from_ip(conn, dbname, collname,
                                    {'IP': gethostbyname(logdict['sys']), 'Exit_time': ''}),
            'System': [logdict['sys']],
            'Question No': [logdict['q']],
            'Question Head': [qnfp.readline().strip()],
            'Hash': [logdict['hash']]
        }
        df = pd.DataFrame(log)
        f = open(logfile, 'a')
        size = f.tell()
        f.close()
        df.to_csv(logfile, mode='a', index=False, header=(size == 0))
        #logfd.write(f"IP: {logdict['system']} question: {logdict['q']} "
        #            f"question_head: {qnfp.readline().strip()} "
        #            f"hash: {logdict['hash']}\n")
    except Exception as arg:
        printerr('exception writing log:', arg)

def send_file(sock, file):
    if not os.path.isfile(file):
        printerr(f'{file} is not a file')
        return

    f = open(file, 'rb')
    print(f'\tsending file {file}', flush=True)
    digest = hashlib.sha256()
    buf = f.read(myconstants.BUFFSIZE)
    while len(buf) != 0:
        digest.update(buf)
        print(f'\tsent {sock.send(buf)} bytes', flush=True)
        buf = f.read(myconstants.BUFFSIZE)
    print(f'\thash: {digest.hexdigest()}', flush=True)
    return digest.hexdigest()

def send_questions(order, port, qdir, logfile=myconstants.LOGFILE, verbose=False,
                   mongo_url=myconstants.MONGO_URL):
    # connect to mongodb to get student name from IP
    conn = None
    try:
        conn = pymongo.MongoClient(mongo_url)
        print('[-] connected to mongodb')
    except Exception as arg:
        printerr(f'[*] error connecting to database: {mongo_url}:', arg)

    try:
        logfd = open(logfile, 'a')
        logfd.close()
    except Exception as arg:
        print("error opening'", logfile, ":", arg)
        sys.exit(2)

    sent = ''
    failed = ''
    for i in order.keys():
        try:
            print(f'[-] trying {i}:{port}', flush=True)
            s = connect_server(i, port)
            print('\tSUCCESS', flush=True)
            qpath = os.path.join(qdir, order[i])
            filesig = send_file(s, qpath)
            # todo: write log as a csv file
            logdict = {'sys': i, 'q': order[i], 'hash': filesig, 'qpath': qpath}
            sent += f"System: {logdict['sys']} Question: {logdict['q']}\n"
            logwrite(logfile, logdict, conn)
            s.close()
        except Exception as arg:
            failed += f'{i}: {arg}\n'
            printerr(f'\tFAILED: {arg}')

    if sent != '':
        print('\nSummary\n'
              '=======\n'
              'SUCCESS\n'
              '=======\n', sent, sep='', flush=True)
    if failed != '':
        printerr('FAILED\n=======\n', failed, sep='')
    print()

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='destination port', default=myconstants.PORT)
    parser.add_argument('-l', '--list',
                        help='filename listing the IPs/hostnames in order', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')
    parser.add_argument('-q', '--questions-dir',
                        help='directory which contains the question files', required=True)
    parser.add_argument('-L', '--logfile',
                        help='file to save logs (questions sent to system) to',
                        default=myconstants.LOGFILE)
    args = parser.parse_args()

    if not os.access(args.list, os.R_OK):
        printerr('cannot access list file', args.list)
        sys.exit(1)
    if not os.access(args.questions_dir, os.R_OK):
        printerr('cannot access questions directory:', args.questions_dir)
        sys.exit(1)
    if not os.path.isdir(args.questions_dir):
        printerr(args.questions_dir, 'is not a directory')
        sys.exit(1)

    if args.verbose:
        print('[-] reading IPs/hostname from file:', args.list,
              '\n[-] questions directory:', args.questions_dir,
              '\n[-] destination port:', args.port,
              '\n[-] log file:', args.logfile, flush=True)

    return args

def main():
    args = argparser()
    iplist = getips(args.list)
    questions = os.listdir(args.questions_dir)

    assignments = assign_questions(iplist, questions)

    send_questions(assignments, args.port, args.questions_dir,
                   logfile=args.logfile, verbose=args.verbose)

if __name__ == '__main__':
    main()
