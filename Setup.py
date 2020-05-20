# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 17:36:44 2019

@author: Ray
"""
import sqlite3
import hashlib
from random import randint
import numpy

conn = sqlite3.connect('trafficdatabase.db')
c = conn.cursor()


def random_digits(num_length):
    
    range_start = 10**(num_length-1)
    range_end = (10**num_length)-1
    
    return randint(range_start, range_end)

c.execute('CREATE TABLE LoginsLog (SessionID INTEGER PRIMARY KEY AUTOINCREMENT, Username TXT, MagicIdentifier INT, Login DATETIME, Logout DATETIME)')
c.execute('CREATE TABLE UsernameLogin (Username TXT, Password TXT)')
c.execute('CREATE TABLE VehicleRecord (RecordID INTEGER PRIMARY KEY AUTOINCREMENT, MagicIdentifier INT, Username TXT, Location TXT, Vehicle TXT, Occ1 INT, Occ2 INT, Occ3 INT, Occ4 INT, DateTime DATETIME, Undone INT)')


numpy.random.seed(100)
for i in range(1, 11):
    c.execute('INSERT INTO UsernameLogin (Username, Password) values(?,?)', ('test'+str(i), hashlib.md5('salt'.encode('utf-8') + ('password'+str(i)).encode('utf-8')).hexdigest()))