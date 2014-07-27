from __future__ import print_function
import sqlite3 as sql
from defervotetree import DeferTree

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

def get_connection_info(data):
    """ Build a tree and determine the connections
        -Check Database for existing tree, if no tree, generate off data
        -if tree found then retrieve tree and rebuild python DS from database
        entries """
    return DeferTree(data=data)

def quote(s):
    return '"%s"' % s

def get_json():
    data = get_vote_info()
    tree = get_connection_info(data)
    nodes = []
    print(str(data))
    print(str(tree))

    nodes = [{quote('name'): quote(x[0]), quote('votes'):1, quote('vote'):quote(x[1])} for x in data]
    edges = [{quote('source'): x[0], quote('target'): x[1]} for x in tree.Edges]
    
    return dict_to_json(nodes, edges)

def dict_to_json(nodes, edges):
    return '{"nodes":['\
    + ','.join(['{' + ','.join(['%s:%s' % kv for kv in d.iteritems()]) + '}' for d in nodes])\
    + '],"links":['\
    + ','.join(['{' + ','.join(['%s:%s' % kv for kv in d.iteritems()]) + '}' for d in edges])\
    + ']}'

def sanitize_inputs(name, vote, defer):
    return (name, vote, defer)
