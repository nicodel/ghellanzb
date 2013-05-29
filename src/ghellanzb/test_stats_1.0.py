#!/usr/bin/env python

#
# python ghellanzb statistics module
#

import ghellanzb_statistics as stats
from time import gmtime, strftime

print 'current directory is :   %s' % stats.home_dir
print 'latest file :            %s' % stats.latest_file
print '\n'

"""
print 'Write the latest value'
stats.write_latest(345)
print '\n'
"""

print 'Get the latest value'
date, value = stats.get_latest()
hour = date[-5:]
date = date[:9]
print 'date :   %s' % date
print 'hours :  %s' % hour
print 'value :  %s' % value

today = strftime('%Y%m%d')

if today != date :
    print '\nLatest stat are not from today'
    response = stats.write_to_disk(date, value)
    if response == True:
        print 'Save successfull'
    else:
        print 'Problem while saving'
else :
    print '\nLatest stats are from today'