from __future__ import print_function
import sqlite3 as sql

def submit_vote(name, vote, defer):
    con = None
    try:
        con = sql.connect('test.db')
        
        cur = con.cursor()
        cur.execute('INSERT INTO Votes VALUES (?,?,?)', sanitize_inputs(name, vote, defer))
        con.commit()

    except sql.Error as e:
        print("Error: %s" % e.args[0])
        return
    
    finally:
        if con:
            con.close()

def get_vote_info():
    try:
        con = sql.connect('test.db')

        cur = con.cursor()
        cur.execute('SELECT Name, Vote, Defer FROM Votes')
        
        return cur.fetchall()

    except sql.Error as e:
        print("Error: %s" % e.args[0])
        return None

    finally:
        if con:
            con.close()

def get_connection_info():
    """ Build a tree and determine the connections """

def quote(s):
    return '"%s"' % s

def get_json():
    data = get_vote_info()
    conlist = get_connection_info(data)
    entries = []
    print(str(data))

    for x in data
        entries.append({quote('name'): quote(x[0]), quote('votes'):1})

def dict_to_json(dlist, conlist):
    return '{"nodes":[' \
    + ','.join(['{' + ','.join(['%s:%s' % kv for kv in d.iteritems()]) + '}' for d in dlist])\
    + '],links:['\
    + ']}'

def sanitize_inputs(name, vote, defer):
    return (name, vote, defer)
