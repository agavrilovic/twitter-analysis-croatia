#!/usr/bin/python

""" A simple class that downloads and stores tweets from Croatia to a file
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
import sys
from sets import Set
import getopt
import time

class GetUsers:

    def __init__(self, auth_ck=None, auth_cs=None, auth_atk=None, auth_ats=None):
        self.myComm = twitterCommunication.TwitterCommunication(auth_ck, auth_cs, auth_atk, auth_ats)
        
    def GetAllFollowersAsObjects(self, username=None):        
        followersToReturn = []
        followerIDs = []    
        while followerIDs == []:
            followerIDs = self.myComm.getIDsOfUsersFollowers(username)
        numberOfFollowers = 0
        for i in followerIDs:
            numberOfFollowers+=1
        print "Total users to request:",numberOfFollowers
        n = 0
        idList = list() #API demands a list
        for followerID in followerIDs:
            idList.append(followerID)
            self.checkRequestLimit()
            followerArray = []
            while followerArray == []:
                followerArray = self.myComm.getUserByID(idList)
            for follower in followerArray:
                followersToReturn.append(follower)
                n+=1
            del idList[:]
        return followersToReturn
            

    def checkRequestLimit(self):
        rateLimit = self.myComm.getRateLimitStatus()
        rateLimit = []
        print "Requests this hour:",rateLimit['remaining_hits']
        while rateLimit == []:
            rateLimit = self.myComm.getRateLimitStatus()
        while rateLimit['remaining_hits'] == 0:
                wait = rateLimit['reset_time_in_seconds']-time.time()
                print "Waiting for Twitter to grant requests:",wait,"s"
                if wait >= 180:
                    time.sleep(180)
                elif wait > 0:
                    time.sleep(wait)
                else:
                    break    


    def depthLoop(self, depth=0, username=None):
        allFollowers[0]=[username]
        if username == None or depth == 0:
            return allFollowers
        for d in range(depth):
            for follower in allFollowers[d]:
                allFollowers[d+1] = self.getAllFollowersAsObjects(follower)
        allFollowersSet = Set()
        for f in allFollowers:
            for u in f:
                allFollowersSet.add(u)
        return allFollowersSet

def main():
    arg = getopt.getopt(sys.argv[1:],"")[1]
    getUsers = GetUsers(arg[0],arg[1],arg[2],arg[3])
    print getUsers.depthLoop(arg[4],arg[5])

if __name__ == "__main__":
    main()