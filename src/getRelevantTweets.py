#!/usr/bin/python

""" A class for downloading tweets from users relevant to Croatian politics
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
import getopt
import sys
import time

class GetRelevantTweets:
    
    def __init__(self, auth_ck=None, auth_cs=None, auth_atk=None, auth_ats=None):        
            self.myComm = twitterCommunication.TwitterCommunication(auth_ck,auth_cs,auth_atk,auth_ats)

    def checkRequestLimit(self):
        rateLimit = self.myComm.getRateLimitStatus()
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
                    
    def getRelevantTimelines(self, fileWithRelevantNames):
        array = []
        relevantUsers = [line.strip() for line in open(fileWithRelevantNames,'r')]
        for relevantUser in relevantUsers:
            self.checkRequestLimit()
            array.append(self.myComm.getTimeline(relevantUser))
        return array


def main():
    arg = getopt.getopt(sys.argv[1:],"")[1]
    getRelevantTweets = GetRelevantTweets(arg[0],arg[1],arg[2],arg[3])
    for timeline in getRelevantTweets.getRelevantTimelines(arg[4]):
        for tweet in timeline:
            print tweet.text.encode("ascii","ignore")
    

if __name__ == "__main__":
    main()
