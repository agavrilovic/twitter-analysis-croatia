#!/usr/bin/python

import csv
import sys
import twitterDB

class Status:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

        
def csvToDictionary(csvFilename):
    csvFile = open(csvFilename,'rb')
    tweetReader = csv.reader(csvFile, delimiter=',', quotechar='\"')
    firstRow = tweetReader.next()
    tweets = []
    for row in tweetReader:
        myDictionary = dict(zip(firstRow, row))
        tweets.append(myDictionary)
    return tweets

def csvToObject(csvFilename):
    csvFile = open(csvFilename,'rb')
    tweetReader = csv.reader(csvFile, delimiter=',', quotechar='\"')
    firstRow = tweetReader.next()
    tweets = []
    for row in tweetReader:
        myDictionary = dict(zip(firstRow, row))
        tweet = Status(**myDictionary)
        tweets.append(tweet)
    return tweets
        

if __name__ == "__main__":
    try:
        csvFilename = sys.argv[1]
    except IndexError:
        csvFilename = "tweets.csv"
    print csvToDictionary(csvFilename)