#!/usr/bin/python

import twitterCommunication
import time

if __name__ == "__main__":
    TC = twitterCommunication.TwitterCommunication()
    limit = TC.getRateLimitStatus()
    print "Remaining hits:",limit['remaining_hits']
    print "Reset time:",limit['reset_time']
    print limit['reset_time_in_seconds']-time.time()