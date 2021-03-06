﻿#!/usr/bin/python

""" A class that stores a list of user objects (followers) in a text file
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
import sys
import time


class GetAllFollowersAsObjects:

    def __init__(self, file, arg=None):        
        myComm = twitterCommunication.TwitterCommunication()
        myDB = twitterDB.TwitterDB(file)

        if arg == "help":
            sys.exit("Use like this: python getAllFollowers.py [file] [userID]")

        followerIDs = []    
        if arg == None:
            fileWithIDs = open("tempIDs.txt","r")
            followerIDs = fileWithIDs.readlines()
            fileWithIDs.close()
        for i in followerIDs:
            followerIDs[n] = int(followerIDs[n].rstrip())        
        else:
            while followerIDs == []:
                followerIDs = myComm.getIDsOfUsersFollowers(arg)
        n = 0
        for i in followerIDs:
            n+=1
        print "Total users to request:",n
        n = 0
        idList = list() #API demands a list
        for followerID in followerIDs:
            if myDB.containsUserID(followerID):
                print "Database already contains",followerID
                continue
            idList.append(followerID)
            rateLimit = []
            while rateLimit == []:
                rateLimit = myComm.getRateLimitStatus()
            print "Requests this hour:",rateLimit['remaining_hits']
            while rateLimit['remaining_hits'] == 0:
                wait = rateLimit['reset_time_in_seconds']-time.time()
                print "Waiting for Twitter to grant requests:",wait,"s"
                if wait >= 180:
                    time.sleep(180)
                elif wait > 0:
                    time.sleep(wait)
                else:
                    break
            followerArray = []
            while followerArray == []:
                followerArray = myComm.getUserByID(idList)
            for follower in followerArray:
                myDB.addUser(follower)
                n+=1
                print n,"Added user ID",followerID,"with name",
                print follower.screen_name.encode('utf-8', 'ignore')        
            del idList[:]


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "listOfObjectsOfFollowersOfVladaRH.dat" #defaults to this output file
    try:
        IDs = sys.argv[2]
    except IndexError:
        IDs = None #defaults to fetching from a file called "tempIDs.txt" (see below)

    GetAllFollowersAsObjects(filename,IDs)
    