#!/usr/bin/env python3

import os
import sys
import random
import argparse

def printerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getips(iplist):
    f = open(iplist, 'r')
    iplst = [ip.strip() for ip in f.readlines()]
    return iplst

def check_order(order):
#    print(order)
    size = len(order)
    for i in range(len(order)):
        prev1 = i - 1
        prev2 = i - 2
        next1 = i + 1
        next2 = i + 2
        if prev1 > 0 and prev1 < size:
            if order[prev1] == order[i]:
                return False
        if prev2 > 0 and prev2 < size:
            if order[prev2] == order[i]:
                return False
        if next1 < size:
            if order[next1] == order[i]:
                return False
        if next2 < size:
            if order[next2] == order[i]:
                return False
    return True

def assign_questions(ips, qns):
    if len(ips) > 2 and len(qns) <= 2:
        printerr(f'not enough questions ({len(qns)}) for ({len(ips)}) systems')
        return {}
    first  = ''
    second = ''
    order = []
    assignment = {}
    for ip in ips:
        # Remove questions that have been assigned to two previous students
        qcopy = qns.copy()
        if first in qcopy:
            qcopy.remove(first)
        if second in qcopy:
            qcopy.remove(second)

        nxt = random.choice(qcopy)
        assignment[ip] = nxt
        first = second
        second = nxt
#        print(ip, nxt)

    return assignment

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        help='filename listing the IPs/hostnames in order', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')
    parser.add_argument('-q', '--questions-dir',
                        help='directory which contains the question files', required=True)
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
        print('[-] reading IPs/hostname from file:', args.list)
        print('[-] questions directory:', args.questions_dir)

    return args

def main():
    args = argparser()
    iplist = getips(args.list)
    questions = os.listdir(args.questions_dir)

    assignments = assign_questions(iplist, questions)
    if args.verbose:
        print(assignments)
    # relies on dictionaries maintaining order of insertion; true for >=3.7
    valid = check_order(list(assignments.values()))
    exit(0 if valid else 1)

if __name__ == '__main__':
    main()

