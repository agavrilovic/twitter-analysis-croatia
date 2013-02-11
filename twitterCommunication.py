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
#def GetFriends(self, user=None, userid=None, cursor=-1, maxUsers=100):


class twitterError(Exception):

    def __init__(self,Exception):
        print "Twitter sent a message:",Exception.message
        #sys.exit("Process terminating.")
        
        
class TwitterCommunication:
    
    def __init__(self):        
        try:
            authFile = open("authorisation.txt",'r')
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

    def getIDsOfUsersFollowers(self, id): #does not work suddenly
        bigData = []
        try:
            data = self.api.GetFollowerIDs(userid=id,cursor=-1)
        except twitter.TwitterError as e:
            twitterError(e)
            return bigData
        try:
            bigData.extend(data['ids'])
        except KeyError:
            print "There was an error fetching the data:",data
            return bigData
        while(data['next_cursor']!=0):
            try:
                data = self.api.GetFollowerIDs(user=username,cursor=data['next_cursor'])
            except twitter.TwitterError as e:
                twitterError(e)
            try:
                bigData.extend(data['ids'])
            except KeyError:
                print "There was an error fetching the data:",data
                return bigData            
        return bigData
        
    def getIDsOfUsersFollowedByUser(self, username):
        bigData = []
        try:
            data = self.api.GetFriendIDs(user=username,cursor=-1)
        except twitter.TwitterError as e:
            twitterError(e)
            return []
        bigData.extend(data['ids'])
        while(data['next_cursor']!=0):
            try:
                data = self.api.GetFriendIDs(user=username,cursor=data['next_cursor'])
            except twitter.TwitterError as e:
                twitterError(e)
            bigData.extend(data['ids'])
        return bigData

    def getUsersFollowedByUser(self, username,i=-1):
        try:
            array = list(self.api.GetFriends(username,maxUsers=i))
        except twitter.TwitterError as e:
            twitterError(e)
        return array

    def getUserByName(self, username):
        return self.api.GetUser(username)
        
    def getUserByID(self, id):
        return self.api.UsersLookup(user_id=id)

    
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
        if arg[2]=="ids":
            array = connection.getIDsOfUsersFollowedByUser(arg[3])
            for k in array:
                print k
        else:
            names = []
            try:
                array = connection.getUsersFollowedByUser(arg[2],int(arg[3]))
            except ValueError:
                array = []
                print "Third argument value must be integer."
            for k in array:
                names.append(k.screen_name)
            for k in names:
                try:
                    print k
                except UnicodeEncodeError:
                    print k.encode('utf-8', 'ignore'),
    else:
        print "Commands:"
        print "\"followers X [Y|-1]\" to print page Y of Xs followers"
        print "\"followers ids X\" to print all IDs X follows" 
        print "\"newest X\" to print the newest tweet of X"
        print "\"where X Y\" to print the location of the user Xs tweet Y"


if __name__ == "__main__":
    main()
