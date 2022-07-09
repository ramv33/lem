#!/usr/bin/env python3

import os
import random

def getips(iplist):
    f = open(iplist, 'r')
    iplst = [ip.strip() for ip in f.readlines()]
    return iplst

def check_order(order):
    print(order)
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
        print(ip, nxt)

    return assignment

def main():
    iplist = getips('iplist')
    questions = os.listdir('qns')

    assignments = assign_questions(iplist, questions)
    # relies on dictionaries maintaining order of insertion; true for >=3.7
    valid = check_order(list(assignments.values()))
    print(valid)
    exit(0 if valid else 1)

if __name__ == '__main__':
    main()
