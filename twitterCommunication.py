#!/usr/bin/python

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
#line:2666  def GetFollowers(self, page=None, cursor=-1): #added param cursor
#line 2685     parameters['cursor'] = cursor
#line 2690:     return data #removed creation of a list of User, just jsonclass TwitterDB:

class twitterError(Exception):

    def __init__(self,Exception):
        print "Twitter sent a message:",Exception.message[0]['message']
        sys.exit("Process terminating.")
        
        
class TwitterCommunication:    
    
    def __init__(self,ck=None, cks=None, at=None, ats=None):
        self.api = twitter.Api(consumer_key=None,consumer_secret=None,
                          access_token_key=None, access_token_secret=None)
        
    def getTweet(self, username, tweetID):
        try:
            array = self.api.GetUserTimeline(username)
        except twitter.TwitterError as e:
            twitterError(e)
        return array[tweetID]

    def getTweetText(self, username, tweetID):
        try:
            array = self.api.GetUserTimeline(username)
        except twitter.TwitterError as e:
            twitterError(e)
        return array[tweetID].text

    def getTweetPlace(self, username, tweetID):
        array = self.api.GetUserTimeline(username)
        return array[tweetID].place

    def getTimeline(self, username):
        array = self.api.GetUserTimeline(username)
        return array

    def getUser(self, username):
        return self.api.GetUser(username)

    def getFollowers(self, username):
        array = self.api.GetFriends(username)
        return array
    
    def getFollowersNames(self, username):
        names = []
        array = self.api.GetFriends(username)
        for k in array:
            names.append(k.screen_name)
        return names

        
def main():
    connection = TwitterCommunication()
    if sys.argv[1]=="help":
        print "Commands:"
        print "\"X follows\" to print out all the users X follows!"
        print "\"newest X\" to print out the newest Tweet of X!"
        print "\"where X\" to print out if X has a known location!"
    if sys.argv[1]=="newest":
        print connection.getTweetText(sys.argv[2], 0)
    if sys.argv[1]=="where":
        if (connection.getUser(sys.argv[2]).geo_enabled == True):
            print "The user has enabled geotagging, printing locations:"
            place=connection.getTweetPlace(sys.argv[2], 1)['name']
            if place!=None:
                print place
            else:
                print "Location not specified"
        else:
            print "GEO not enabled"
    try:
        if sys.argv[2]=="follows":
            print connection.getFollowersNames(sys.argv[1])
    except IndexError:
        pass

        
if __name__ == "__main__":
    main()
