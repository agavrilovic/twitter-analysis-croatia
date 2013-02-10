#!/usr/bin/python

""" A class that downloads and stores a list of followers in a text file
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
import time

def getAllFollowers():
    MAX = 1000 #arbitrary
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = "VladaRH" #defaults to this account
    try:
        file = sys.argv[2]
    except IndexError:
        file = "followersVladaRH.txt" #defaults to this file

    myComm = twitterCommunication.TwitterCommunication()
    myDB = twitterDB.TwitterDB(file)
    if arg != "help":
        followers = myComm.getUser(arg).followers_count
        if followers<MAX: #users with little or no followers -> directly
            print "Using GetFollowers"
            users = myComm.getFollowers(arg,followers)
            for k in users:
                myDB.addUser(k)
        else:
            print "Using ID lookup"
            users = myComm.getFollowersIDs(arg)

            n = 0
            for u in users:
                n+=1
                id = list()
                id.append(u)
                user = myComm.getUserByID(id)
                del id[:]
                for k in user:
                    myDB.addUser(k)
                    print n,"Added user ID",u,"with name",k.screen_name
                time.sleep(25)
    else:
        print "Use like this: python getAllFollowers.py [user] [file]"

if __name__ == "__main__":
    getAllFollowers()