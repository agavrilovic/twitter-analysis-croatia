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
import sys
import urllib2

#Changes made to python-twitter library (v.0.9) to enable pagination:
#def GetFriends(self, user=None, userid=None, cursor=-1, maxUsers=100):
#def GetFollowers(self, user=None, page=None):

class twitterError(Exception):

    def __init__(self,Exception):
        print "Twitter sent a message:",Exception.message[0]['message'], "; Code:",Exception.message[0]['code']
        if Exception.message[0]['code']==34:
            sys.exit("Unknown user, process terminating.")
        
        
class TwitterCommunication:
    
    def __init__(self):        
        try:
            authFile = open("authorisation",'r')
            auth_ck = authFile.readline().rstrip()
            auth_cs = authFile.readline().rstrip()
            auth_atk = authFile.readline().rstrip()
            auth_ats = authFile.readline().rstrip()
            authFile.close()
            self.api = twitter.Api(
                consumer_key=auth_ck, 
                consumer_secret=auth_cs,
                access_token_key=auth_atk, 
                access_token_secret=auth_ats)
        except IOError:
            self.api = twitter.Api()

    def getTimeline(self, username=None):
        array = []
        if username == None:
            print "getTimeline: Argument needed: username"
            return array
        try:
            array = self.api.GetUserTimeline(username)
        except twitter.TwitterError as e:
            twitterError(e)
        return array

    def getTweet(self, username=None, tweetID=0):
        if username == None:
            print "getTweet: Argument needed: username"
            return None
        array = self.getTimeline(username)
        if array != []:
            return array[tweetID]
        else:
            return None

    def getTweetText(self, username=None, tweetID=0):
        if username == None:
            print "getTweetText: Argument needed: username"
            return None
        tweet = self.getTweet(username,tweetID)
        if tweet != None:
            return tweet.text
        else:
            return None

    def getTweetPlace(self, username=None, tweetID=0):
        if username == None:
            print "getTweetPlace: Argument needed: username"
            return None
        tweet = self.getTweet(username,tweetID)
        if tweet != None:
            if tweet.place != None:
                return tweet.place
        return None

    def getIDsOfUsersFollowers(self, username):
        bigData = []
        if username == None:
            print "getIDsOfUsersFollowers: Argument needed: username"
            return bigData        
        try:
            data = self.api.GetFollowerIDs(user=username,cursor=-1)
        except twitter.TwitterError as e:
            twitterError(e)
            return []
        except urllib2.URLError as e:
            print e
            return []
        bigData.extend(data['ids'])
        while(data['next_cursor']!=0):
            try:
                data = self.api.GetFollowerIDs(user=username,cursor=data['next_cursor'])
            except twitter.TwitterError as e:
                twitterError(e)
            except urllib2.URLError as e:
                print e
            bigData.extend(data['ids'])
        return bigData
        
    def getIDsOfUsersFollowedByUser(self, username=None):
        bigData = []
        if username == None:
            print "getIDsOfUsersFollowedByUser: Argument needed: username"
            return bigData        
        try:
            data = self.api.GetFriendIDs(user=username,cursor=-1)
        except twitter.TwitterError as e:
            twitterError(e)
            return []
        except urllib2.URLError as e:
            print e
            return []
        bigData.extend(data['ids'])
        while(data['next_cursor']!=0):
            try:
                data = self.api.GetFriendIDs(user=username,cursor=data['next_cursor'])
            except twitter.TwitterError as e:
                twitterError(e)
            except urllib2.URLError as e:
                print e
            bigData.extend(data['ids'])
        return bigData

    def getUserByName(self, username):
        try:
            return self.api.GetUser(username)
        except urllib2.URLError as e:
            print e
            return []
        
    def getUserByID(self, id):
        try:
            user = self.api.UsersLookup(user_id=id)
        except AttributeError as e:
            print e
            return []
        except urllib2.URLError as e:
            print e
            return []
        return user

    def getRateLimitStatus(self):
        try:
            return self.api.GetRateLimitStatus()
        except urllib2.URLError as e:
            print e
            return []
    
def main():
    arg = [""]*4
    try:
        arg[1] = sys.argv[1]
    except IndexError:
        arg[1] = "help"
    try:
        arg[2] = sys.argv[2]
    except IndexError:
        arg[2] = ""

    connection = TwitterCommunication()

    if arg[1] == "newest":
        try:
            print connection.getTweetText(arg[2], 0)
        except UnicodeEncodeError:
            print connection.getTweetText(arg[2], 0).encode('utf-8', 'ignore')
    elif arg[1] == "where" and arg[2] != "":
        noneFound = True
        i=0
        while 1:
            i+=1
            try:
                place = connection.getTweetPlace(arg[2], i)
            except urllib2.URLError as e:
                print e
                break
            except IndexError as e:
                print "Browsed through entire timeline."
                break
            if place != None:
                noneFound = False
                print "Tweet #",i,":",
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
        if noneFound:
            print "No locations available for this account."
    
    elif arg[1] == "friends" and arg[2] != "":
        array = connection.getIDsOfUsersFollowedByUser(arg[2])
        for k in array:
            print k
    elif arg[1] == "followers" and arg[2] != "":
        array = connection.getIDsOfUsersFollowers(arg[2])
        for k in array:
            print k
    else:
        print "Commands:"
        print "\"friends X\" to print all IDs X follows" 
        print "\"followers X\" to print all IDs that follow X"         
        print "\"newest X\" to print the newest tweet of X"
        print "\"where X\" to print the locations of the user Xs last tweets"


if __name__ == "__main__":
    main()
