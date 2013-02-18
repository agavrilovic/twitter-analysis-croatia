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
        sys.exit("Process terminating.")

class TwitterDB:

    database = None

    def __init__(self,database):
        self.database=database
        open(self.database,'ab').close()        
        
    def addTweet(self,newTweet):
        tweets = self.getTweets()
        for tweet in tweets:
            if tweet.id == newTweet.id:
                return False
        db = open(self.database,'ab')
        pickle.dump(newTweet,db)
        db.close()
        return True

    def addUser(self,newUser):
        users = self.getUsers()
        for user in users:
            if user.id == newUser.id:
                return False
        db = open(self.database,'ab')
        pickle.dump(newUser,db)
        db.close()
        return True

    def containsUserID(self,query):
        users = self.getUsers()
        for user in users:
            if user.id == query:
                return True
        return False
        
    def getTweets(self):
        db = open(self.database,'rb')
        array = []
        while(1):
            try:
                tweet = pickle.load(db)
            except EOFError:
                db.close()
                return array
            array.append(tweet)
        return None

    def getUsers(self):
        return self.getTweets()
		
    def getTweet(self,username):
        db = open(self.database,'rb')
        entry = None
        while(1):
            try:
                tweet = pickle.load(db)
            except EOFError:
                db.close()
                return entry
            if tweet.user.screen_name==username:
                return tweet
        return None

    def getAllTweetsFromUser(self,username):
        db = open(self.database,'rb')
        array = []
        while(1):
            try:
                tweet = pickle.load(db)
            except EOFError:
                db.close()
                return array
            if tweet.user.screen_name==username:
                array.append(tweet)
        return None

def main():
    arg = [""]*5
    try:
        arg[1] = sys.argv[1]
    except IndexError:
        arg[1] = "help"
    try:
        arg[2] = sys.argv[2]
    except IndexError:
        arguemnt[2] = ""
    try:
        arg[3] = sys.argv[3]
    except IndexError:
        arg[3] = ""
    try:
        arg[4] = sys.argv[4]
    except IndexError:
        arg[4] = ""

	myDB = TwitterDB(arg[1])
    
    if arg[2]=="get":
        if arg[3]=="all":
            if arg[4]=="":
                for tweet in myDB.getTweets():
                    print tweet.text
            else:
                for tweet in myDB.getAllTweetsFromUser(arg[4]):
                    print tweet.text
        else:
            print myDB.getTweet(arg[2]).text
    else:
        print "Use twitterDB like this: "
        print "python twitterDB.py file get \[all\] \[USER\] to print tweets"
        
if __name__ == "__main__":
    main()