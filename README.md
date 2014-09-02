## Introduction

This project provides a very basic database access layer for MySQL/Maria databases.

It aims to be minimalist while maintaining high database performance.

## Prerequisites

* [MySQL-python](https://pypi.python.org/pypi/MySQL-python/1.2.5)

```bash
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Tests

```bash
python tests/test.py
```


## Usage

### Configuration

The public functions all expect to be passed a hash containing the database
connection information. In this example we have added the connection parameters
to the config class itself as a nice handy container, however there is no reason 
why these cant be stored in your own configuration section.

```python
# Add to config.py
class db(object):

    # Place your database connections here
    Test      = {'db':"test"      , 'host':"localhost" , 'user':'www' , 'password':'www'}
    Customers = {'db':"customers" , 'host':"localhost" , 'user':'www' , 'password':'www'}
```

### Accessing the database

All database access functions are static methods that return results, there is no need 
to instantiate a class.

Make sure to import the config and database modules

```python
from databases.dba import dba
from config import db
```

#### No result queries

This function provides a simple api to run any query where a return value from the
database is not expected, for example, INSERT, UPDATES and DELETES. It returns a
tuple containing new identifiers and rows affected.

```python
new_id, rows_affected = dbaempty( query, params, database )
```

Example

```python
dbaempty( "CREATE DATABASE IF NOT EXISTS test" , None, db.Test )
dbaempty( "DROP TABLE IF EXISTS Authors" , None, db.Test )
dbaempty( "CREATE TABLE Authors(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25)) ENGINE=INNODB" , 
            None, db.Test )

print "Inserting new row, id: %s, rows affected: %s" % dbaempty(
    "INSERT INTO Authors ( Name ) VALUES ( %s )",
    ("Text Single Quote's",),
    db.Test
)
```

#### Single results

This function provides a convenient way to get a single result, such as a row count

```python
result = dbascalar( query, params, database )
```

Example

```python
print "Testing scalar query, total authors currently in db: ", dbascalar("SELECT Count(*) FROM Authors", None, db.Test)
```
#### Dictionary result

The function returns an array of dictionary results


```python
results = dbadict( query, params, database )
```

Example

```python
for author in dbadict('SELECT Id, Name FROM Authors', None, db.Test):
    print "Author; %s" % author['Name']
```

#### JSON result

The function returns a JSON object containing the results

```python
results = dbajson( query, params, database )
```

Example

```python
print  "List of current authors: ", 
       dbajson('SELECT * FROM Authors', None, db.Test)
```

#### Multiple transactions

This function allows for the execution of multiple queries which will be groups
into a single transaction, if one failes then the whole lot will be rolled
back. The results is aa tuple of the (new_id, rows_affected) for each query -
in order of the original list of queries.

```python
results = dbatransaction( ( (query, params), .. ), database )
```

Simple Example
```python
setup = (
     ("INSERT INTO Authors ( Name ) VALUES ( 'Jane Watts'        )" , None ),
     ("INSERT INTO Authors ( Name ) VALUES ( 'Stephen Donaldson' )" , None ),
)

print "List of new identifiers and rows affected", dba.transaction(setup, db.Test)
```

More Complex Example with params
```python
setup = (
    ( "INSERT INTO Authors ( Name ) VALUES ( %s )" ,  ( 'Jack London'       ,  )  ),
    ( "INSERT INTO Authors ( Name ) VALUES ( %s )" ,  ( 'Honore de Balzac'  ,  )  ),
    ( "INSERT INTO Authors ( Name ) VALUES ( %s )" ,  ( 'Lion Feuchtwanger' ,  )  ),
    ( "INSERT INTO Authors ( Name ) VALUES ( %s )" ,  ( 'Emile Zola'        ,  )  ),
    ( "INSERT INTO Authors ( Name ) VALUES ( %s )" ,  ( 'Truman Capote'     ,  )  ),
    ( "INSERT INTO Authors ( Name ) VALUES ( %s )" ,  ( 'Terry Pratchett'   ,  )  ),
)

print "List of new identifiers and rows affected", dbatransaction(setup, db.Test)
```

#### Full Example

```python
from databases.dba import DB
from config import db

print 'Testing MySQL DB Access'

print "Creating database and tables.."
dbaempty( "CREATE DATABASE IF NOT EXISTS test" , None, db.Test )
dbaempty( "DROP TABLE IF EXISTS Authors" , None, db.Test )
dbaempty( "CREATE TABLE Authors(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25)) ENGINE=INNODB" , 
            None, db.Test )


print "Inserting new row, id: %s, rows affected: %s" % dbaempty(
    "INSERT INTO Authors ( Name ) VALUES ( %s )",
    ("Text Single Quote's",), db.Test
)

print "Testing scalar query, total authors currently in db: ", dbascalar("SELECT Count(*) FROM Authors", None, db.Test)

print  "List of current authors: ", dbadict('SELECT * FROM Authors', None,
        db.Test)

print  "List of current authors: ", dbajson('SELECT * FROM Authors', None,
        db.Test)

print "Testing multiple transactions"
setup = (
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Jack London'      ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Honore de Balzac' ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Lion Feuchtwanger',)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Emile Zola'       ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Truman Capote'    ,)),
    ("INSERT INTO Authors ( Name ) VALUES ( %s ) ", ('Terry Pratchett'  ,)),
)

print "List of new identifiers and rows affected", dbatransaction(setup,
        db.Test)


for author in dbadict('SELECT Id, Name FROM Authors', None, db.Test):
    print "Author; %s" % author['Name']

print "Testing scalar query, total authors in db: ", dbascalar("SELECT Count(*) FROM Authors", None, db.Test)
```

