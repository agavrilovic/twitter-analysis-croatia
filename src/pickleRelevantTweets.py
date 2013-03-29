#!/usr/bin/python

""" A class for storing tweets downloaded by getRelevantTweets
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

import twitterDB
import getRelevantTweets
import getopt
import sys
import time

def main():
    while(1):
        arg = getopt.getopt(sys.argv[1:],"")[1] #use like this: authorisation, input file, output file
        myDB = twitterDB.TwitterDB(arg[5])
        myComm = getRelevantTweets.GetRelevantTweets(arg[0],arg[1],arg[2],arg[3])
        for timeline in myComm.getRelevantTimelines(arg[4]):
            for tweet in timeline:
                myDB.addTweet()
        print "Currently in file:",myDB.howManyTweets()
        time.sleep(180)

if __name__ == "__main__":
    main()
