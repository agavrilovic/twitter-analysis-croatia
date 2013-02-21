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
import twitterDB
import getAllFollowersAsObjects
import sys
import threading

class TwitterCroatia:
        
    def __init__(self,userFile="userObjects.dat",twitterFile="tweetsFilename.dat"):
        userObjectsDB = twitterDB.TwitterDB(userFile)
        tweetObjectsDB = twitterDB.TwitterDB(twitterFile)
        myComm = twitterCommunication.TwitterCommunication()
        usernamesPassed = []
        i = 0
        while True:
            arrayOfUserObjects = userObjectsDB.getUsers()
            try:
                username = arrayOfUserObjects[i].screen_name
            except AttributeError:
                print "Encountered an unexpected not-a-user object."
                break
            except IndexError:
                print "No more users to add."
                break
            i+=1
            print "Requesting followers of",username
            if not username in usernamesPassed:
                usernamesFollowers = getAllFollowersAsObjects.GetAllFollowersAsObjects(userFile,username)
                usernamesTimeline = myComm.getTimeline(username)
                for tweet in usernamesTimeline:
                    tweetObjectsDB.addTweet(tweet)
            usernamesPassed.append(username)
            print "All tweets of",username,"added to file",twitterFile
            print "All followers of",username,"added to file",userFile
            print "Total number of users timelines & followers added so far:",i


if __name__ == "__main__":

    try:
        usersFilename = sys.argv[1]
    except IndexError:
        usersFilename = "userObjects.dat" #defaults to this output file for user objects
        myDB = twitterDB.TwitterDB(usersFilename)
        firstUserForDefaultDB = twitterCommunication.TwitterCommunication().getUserByName("sasastartrek")
        myDB.addUser(firstUserForDefaultDB)

    try:
        tweetsFilename = sys.argv[2]
    except IndexError:
        tweetsFilename = "tweetObjects.dat" #defaults to this output file for tweet objects

    TwitterCroatia(usersFilename,tweetsFilename)