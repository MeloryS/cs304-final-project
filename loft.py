#!/usr/bin/python2.7

import sys
import MySQLdb

def getConn(db):
    conn =  MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn

#--Adding to Database-- 
def createUser(conn, name, email, pw, university):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into users values (%s, %s, %s, %s, NULL)''',
                (name, email, pw, university,))
    return curs.fetchone()
    
def createProperty(conn, name, descrip, loc, price, smoker, gender, pet):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into properties values (%s, %s, %s, %s, %s, %s, %s, NULL)''', 
                (name, descrip, loc, price, smoker, gender, pet,))
    return curs.fetchone()

def createDate(conn, PID, start, end):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into dates values (%s, %s, %s)''',
                (PID, start, end,))
    return curs.fetchone()

def addTenantFeature(conn, UID, feature):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into featuresTenants values (%s, %s)''',
                (UID, feature,))
    return curs.fetchone()

def addPropertyFeature(conn, PID, feature):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into featuresProperties values (%s, %s)''',
                (PID, feature,))
    return curs.fetchone()
    
def addHostProp(conn, UID, PID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into host_prop values (%s, %s)''',
                (UID, PID,))
    return curs.fetchone()

# Searching properties based on specific filters
def searchProp(conn, gender, location, price):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if(gender == 3): #no preference
        gender = "1, 2, 3"
    location = "%" + location + "%"
    curs.execute('''select * from properties where gender in (%s) and location like %s and price < %s''',
                (gender, location, price))
    return curs.fetchall()

#updating table values
def updateUser(conn, UID, name, email, pw, university):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''update users set name = %s, email = %s, pw = %s, university = %s where UID = %s''', 
                (name, email, pw, university, UID))
    return curs.fetchone

def updateProperty(conn, PID, name, descrip, loc, price, smoker, gender, pet):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''update properties set name = %s, descrip = %s, loc = %s, price = %s, smoker = %s, gender = %s, pet = %s where PID = %s''', 
                (name, descrip, loc, price, smoker, gender, pet, PID))
    return curs.fetchone

#retrieves last property created based on largest PID value
def getLastProperty(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from properties where PID = (select max(PID) from properties)''')
    return curs.fetchone()

def getAll(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from properties''')
    return curs.fetchall()

def getOne(conn, PID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from properties where PID = %s''', (PID))
    return curs.fetchone()

if __name__ == '__main__':
    conn = getConn('loft')
    # user = createUser(conn, 'Ally', 'ally@tufts.edu', 'Password123', 'Tufts University')
    prop = createProperty(conn, 'House', 'A House in Boston', 'Boston', 800, 0, 1, 0)