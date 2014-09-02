#!/usr/bin/env python
# encoding: utf-8

from databases.dba import dba
from config import db

print db.Test

print 'Testing MySQL DB Access'

print "Creating database and tables.."
dba.empty( "CREATE DATABASE IF NOT EXISTS test" , None, db.Test )
dba.empty( "DROP TABLE IF EXISTS Authors" , None, db.Test )
dba.empty( "CREATE TABLE Authors (Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25) ) ENGINE=INNODB" , None, db.Test )


print "Inserting new row, id: %s, rows affected: %s" % dba.empty(
    "INSERT INTO Authors ( Name ) VALUES ( %s )",
    ("Text Single Quote's",),
    db.Test
)

print "Testing scalar query, total authors currently in db: ", dba.scalar("SELECT Count(*) FROM Authors", None, db.Test)

print  "List of current authors: ", dba.dict('SELECT * FROM Authors', None,
        db.Test)

print  "List of current authors: ", dba.json('SELECT * FROM Authors', None,
        db.Test)

print "Simple transaction example"
setup = (
     ("INSERT INTO Authors ( Name ) VALUES ( 'Jane Watts'        )" , None ),
     ("INSERT INTO Authors ( Name ) VALUES ( 'Stephen Donaldson' )" , None ),
)

print "List of new identifiers and rows affected", dba.transaction(setup, db.Test)

print "Testing multiple transactions"
setup = (
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Jack London'      ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Honore de Balzac' ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Lion Feuchtwanger',)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Emile Zola'       ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Truman Capote'    ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Terry Pratchett'  ,)),
)

print "List of new identifiers and rows affected", dba.transaction(setup,
        db.Test)


for author in dba.dict('SELECT * FROM Authors', None, db.Test):
    print "Author; %s" % author['Name']

print "Testing scalar query, total authors in db: ", dba.scalar("SELECT Count(*) FROM Authors", None, db.Test)

