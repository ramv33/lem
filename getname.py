#!/usr/bin/env python3

import pymongo

def getname_from_ip(conn, dbname, collname, filter_, name='Name'):
    db = conn[dbname]
    coll = db[collname]
    res = coll.find_one(filter_)
    if res is None:
        print('None')
        return ''
    return res['Name']
    
def main():
    conn = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    print(getname_from_ip(conn, 'LMS', 'info', {'IP': '192.168.0.7'}, 'Name'))

if __name__ == '__main__':
    main()
