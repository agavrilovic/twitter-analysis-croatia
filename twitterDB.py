#!/usr/bin/python

""" A simple class that helps store objects in a database using pickle.
    Copyright (C) 2012./2013. Aleksandar Gavrilovic / FER

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
"""

import pickle
import sys #for command line options

class unknownError():
    
    def __init__(self,Exception):
        print "Unexpected error:", Exception


class TwitterDB:

    database = None

    def __init__(self,database):
        self.database=database
        
    def addTweet(self,tweet):
        db = open(database,'a')
        pickle.dump(tweet,db)
        db.close()
		
    def getTweet(self,username):
        db = open(database,'rb')
        entry = []
        while(1):
            try:
                entry = pickle.load(db)
            except EOFError:
                db.close()
                return entry
            except Exception:
                unknownError(Exception)
            if entry.user.name==username:
                db.close()
                return entry
        
    def getAllTweets(self,username):
        db = open(database,'rb')
        array = []
        while(1):
            try:
                entry = pickle.load(db)
            except EOFError:
                db.close()
                return array
            except Exception:
                unknownError(Exception)
            if entry.user.name==username:
                array+=entry

	def getAllTweets(self):
		db = open(database,'rb')
		array = []
        while(1):
            try:
                entry = pickle.load(db)
            except EOFError:
                db.close()
                return array
            except Exception:
                unknownError(Exception)
            array+=entry
        
        
if __name__ == "__main__":
	myDB = TwitterDB(sys.argv[1])
    print myDB.getAllTweets()
