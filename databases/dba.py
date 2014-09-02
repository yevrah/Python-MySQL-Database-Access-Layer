#!/usr/bin/env python
# encoding: utf-8

import MySQLdb as mdb
import sys
import json

# Suppress warnings from MySQL DB
from warnings import filterwarnings
import MySQLdb as Database
filterwarnings('ignore', category = Database.Warning)

class dba(object):

    @staticmethod
    def _query(query, params, database):
        try:
            con = mdb.connect(host=database['host'], user=database['user'],
                    passwd=database['password'], db=database['db'])
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute(query, params)
            rows = cur.fetchall()
        except mdb.Error, e: rows = []
        finally:
            if con:
                con.close()
        return rows;

    @staticmethod
    def dict(query, params, database):
        return dba._query( query, params, database )

    @staticmethod
    def json(query, params, database):
        return json.dumps( dba._query( query, params, database) )

    @staticmethod
    def scalar(query, params, database):
        try:
            con = mdb.connect(host=database['host'], user=database['user'],
                    passwd=database['password'], db=database['db'])
            cur = con.cursor()
            cur.execute(query, params)
            rows = cur.fetchone()[0]
        except mdb.Error, e: rows = 0;
        finally:
            if con:
                con.close()
        return rows

    @staticmethod
    def empty(query, params, database):
        last_id = None
        row_count = None
        try:
            con = mdb.connect(host=database['host'], user=database['user'],
                    passwd=database['password'], db=database['db'])
            cur = con.cursor()
            cur.execute(query, params)
            last_id =  cur.lastrowid
            row_count = cur.rowcount
            con.commit()
        except mdb.Error, e:
            print e
            pass
        finally:
            if con:
                con.close();
        return last_id, row_count

    @staticmethod
    def transaction(queries, database):
        result = []
        try:
            con = mdb.connect(host=database['host'], user=database['user'],
                    passwd=database['password'], db=database['db'])
            cur = con.cursor()
            for query in queries:
                print query
                sql, params = query
                cur.execute(sql, params)
                result.append( (cur.lastrowid, cur.rowcount) )
            con.commit()
        except mdb.Error, e:
            if con:
                con.rollback()
        finally:
            if con:
                con.close()

        return result
