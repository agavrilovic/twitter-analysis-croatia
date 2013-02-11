#!/usr/bin/python

""" A simple module that takes a users tweets and prints out their texts
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

import twitterCommunication
import twitterDB
import sys #for command line options


def main():
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = "help" #defaults to this command
    try:
        user = sys.argv[2]
    except IndexError:
        user = "VladaRH" #defaults to this user
    try:
        if sys.argv[3]=="False":
            verbose=False
        else:
            verbose=True
    except IndexError:
        verbose = True

    if arg == "help":
        print "Use exampleModule like this: "
        print "python exampleModule.py filename [user] [verbosity]"
    
    else:
        myComm = twitterCommunication.TwitterCommunication()
        myDB = twitterDB.TwitterDB(arg)
   
        tweets = myComm.getTimeline(user)
        k=0
        for tweet in tweets:
            if verbose:
                k+=1
                if myDB.addTweet(tweet):
                    print "Tweet",k,"from user",user,"put in database",file
                else:
                    print "Tweet",k,"from user",user,"already in database",file
            else:
                myDB.addTweet(tweet)

        if verbose:
            print "Fetching 1 tweet from user",user,"in database",file
            print myDB.getTweet(user)
            print "Fetching all tweets from user",user,"in database",file
            print myDB.getAllTweetsFromUser(user)
            print "Fetching all tweets from database",file
        
        for tweet in myDB.getTweets():
            print tweet.text        

if __name__ == "__main__":
    main()
