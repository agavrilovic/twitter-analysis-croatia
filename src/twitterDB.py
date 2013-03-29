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
import sys
import getopt

class TwitterDB:

    database = None

    def __init__(self,database):
        self.database=database
        #open(self.database,'ab').close()        
        
    def addTweet(self,newTweet):
        tweets = self.getTweets()
        for tweet in tweets:
            if tweet.id == newTweet.id:
                return False
        try:
            db = open(self.database,'ab')
        except:
            raise DatabaseError
        pickle.dump(newTweet,db)
        db.close()
        return True

    def addUser(self,newUser):
        users = self.getUsers()
        for user in users:
            if user.id == newUser.id:
                return False
        try:
            db = open(self.database,'ab')
        except:
            raise DatabaseError
        pickle.dump(newUser,db)
        db.close()
        return True

    def containsUserID(self,query):
        users = self.getUsers()
        for user in users:
            try:
                if user.id == query:
                    return True
            except AttributeError:
                continue
        return False
        
    def howManyTweets(self):
        tweets = self.getTweets()
        i = 0
        for tweet in tweets:
            i+=1
        return i
        
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
            try:
                if tweet.user.screen_name==username:
                    return tweet
            except AttributeError:
                continue
        return entry

    def getAllTweetsFromUser(self,username):
        db = open(self.database,'rb')
        array = []
        while(1):
            try:
                tweet = pickle.load(db)
            except EOFError:
                db.close()
                return array
            try:
                if tweet.user.screen_name==username:
                    array.append(tweet)
            except AttributeError:
                continue
        return None

def main():
    arg = getopt.getopt(sys.argv[1:],"")[1]
    
    myDB = TwitterDB(arg[0])

    if arg[1]=="get":
        if arg[2]=="all":
            if arg[3]=="":
                for tweet in myDB.getTweets():
                    try:
                        print tweet.text
                    except AttributeError:
                        print "Program ran into unexpected not-a-tweet object."
            else:
                tweets = myDB.getAllTweetsFromUser(arg[4])
                for tweet in tweets:
                    try:
                        print tweet.text
                    except AttributeError:
                        print "Program ran into unexpected not-a-tweet object."
        else:
            print myDB.getTweet(arg[1]).text
    else:
        print "Use twitterDB like this: "
        print "python twitterDB.py file get [all] [USER]"
        
if __name__ == "__main__":
    main()