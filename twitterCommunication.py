﻿#!/usr/bin/python

""" A simple class for downloading data from Twitter using twitter-python
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

import twitter
import sys #for command line options

#Changes made to python-twitter library (v.0.9) to enable pagination:
#entire def GetFollowers(self, page=None, cursor=-1)


class twitterError(Exception):

    def __init__(self,Exception):
        print "Twitter sent a message:",Exception.message
        #sys.exit("Process terminating.")
        
        
class TwitterCommunication:    
    
    def __init__(self,ck=None, cks=None, at=None, ats=None):
        self.api = twitter.Api(consumer_key=None,consumer_secret=None,
                          access_token_key=None, access_token_secret=None)


    def getTimeline(self, username):
        array = []
        try:
            array = self.api.GetUserTimeline(username)
        except twitter.TwitterError as e:
            twitterError(e)
        return array

    def getTweet(self, username, tweetID):
        array = self.getTimeline(username)
        if array != []:
            try:
                return array[tweetID]
            except IndexError:
                print "Timeline exceeded"
                return None
        else:
            return None


    def getTweetText(self, username, tweetID):
        tweet = self.getTweet(username,tweetID)
        if tweet != None:
            return tweet.text
        else:
            return None

    def getTweetPlace(self, username, tweetID):
        tweet = self.getTweet(username,tweetID)
        if tweet != None:
            if tweet.place != None:
                return tweet.place
            print "No location given"
        return None

    def getFollowers(self, username,i):
        try:
            array = list(self.api.GetFriends(username,maxUsers=i))
        except twitter.TwitterError as e:
            twitterError(e)
        return array
    
    def getFollowersNames(self, username,i):
        names = []
        array = self.getFollowers(username,i)
        for k in array:
            names.append(k.screen_name)
        return names

    def getUser(self, username):
        return self.api.GetUser(username)

    
def main():
    arg = [""]*4
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

    connection = TwitterCommunication()

    if arg[1]=="newest":
        try:
            print connection.getTweetText(arg[2], 0)
        except UnicodeEncodeError:
            print connection.getTweetText(arg[2], 0).encode('utf-8', 'ignore')
    elif arg[1]=="where":
        place = connection.getTweetPlace(arg[2], int(arg[3]))
        if place != None:
            try:
                print place['country'],"(",
            except UnicodeEncodeError:
                print place['country'].encode('utf-8', 'ignore'),"(",
            print place['country_code'],"),",
            print place['place_type'],":",
            try:
                print place['name']
            except UnicodeEncodeError:
                print place['name'].encode('utf-8', 'ignore')
    
    elif arg[1]=="followers":
            for k in connection.getFollowersNames(arg[2],int(arg[3])):
                try:
                    print k
                except UnicodeEncodeError:
                    print k.encode('utf-8', 'ignore'),
    
    else:
        print "Commands:"
        print "\"followers X i\" to print out all the users X follows, page i!"
        print "\"newest X\" to print out the newest Tweet of X!"
        print "\"where X Y\" to print out the location of the tweet Y from user X!"


if __name__ == "__main__":
    main()
