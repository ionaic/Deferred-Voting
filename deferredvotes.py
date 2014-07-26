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

def sanitize_inputs(name, vote, defer):
    return (name, vote, defer)
