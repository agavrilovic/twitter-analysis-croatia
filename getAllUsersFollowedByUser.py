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

def getAllUsersFollowedByUser():
    try:
        arg = int(sys.argv[1])
    except IndexError:
        arg = "VladaRH" #defaults to this account
    try:
        file = sys.argv[2]
    except IndexError:
        file = "FriendsOfVladaRH.txt" #defaults to this file

    myComm = twitterCommunication.TwitterCommunication()
    myDB = twitterDB.TwitterDB(file)
    if arg != "help":
        user = []
        while user == []:
            user = myComm.getUserByName(arg)
        friendIDs = []
        while friendIDs == []:
            friendIDs = myComm.getIDsOfUsersFollowedByUser(arg)
        n = 0
        for i in friendIDs:
            n+=1
        print "Total users to request:",n
        n = 0
        idList = list() #API demands a list
        for friendID in friendIDs:
            idList.append(friendID)
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
            friendArray = []
            while friendArray == []:
                friendArray = myComm.getUserByID(idList)
            for friend in friendArray:
                myDB.addUser(friend)
                n+=1
                print n,"Added user ID",friendID,"with name",
                print friend.screen_name.encode('utf-8', 'ignore')
            
            del idList[:]
    else:
        print "Use like this: python getAllFollowers.py [userID] [file]"

if __name__ == "__main__":
    getAllUsersFollowedByUser()
    