#!/usr/bin/python

""" A class that downloads and stores a list of followers locations
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
import sys #for commandline arguments

def whereData():
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = ""
    try:
        file = sys.argv[2]
    except IndexError:
        file = "tweetsCroatia.txt"    
    myComm = twitterCommunication.TwitterCommunication()
    myDB = twitterDB.TwitterDB(file)
    if arg != "":
        followers = myComm.getUser(arg).followers_count
        users = myComm.getFollowers(arg,followers)
        for k in users:
            myDB.addUser(k)
    else if arg != "help":
        for user in myDB.getUsers():
            if user.location!=None:
                print user.location.encode('utf-8', 'ignore')
            else:
                print "None"
    else:
        print "Use like this: python twitterCroatia.py [user] [file]"

if __name__ == "__main__":
    whereData()
