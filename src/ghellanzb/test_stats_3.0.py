#!/usr/bin/env python

import random
import ghellanzb_statistics as stats
from time import gmtime, strftime

""" we get the latest hellanzb total_mb_dl """
date = strftime('%Y%m%d')
value = random.randint(300,4550)

""" we get the value recorded in latest_file """
ldate, lvalue = stats.get_latest()
print 'date :   %s' % ldate
print 'value :  %s' % lvalue

""" we compare today's date and latest date """
today = strftime('%Y%m%d')
if today != ldate[:8] :
    print '\nLatest stat are not from today'
    response = stats.add_new_day(ldate, lvalue)
    if response == True:
        print 'Save successfull'
    else:
        print 'Problem while saving'
    print '\nWriting value to latest'
    response = stats.write_latest(value)
    if response:
        print 'Write latest succesful'
    else:
        print 'Problem while writing latest value'
else :
    print '\nLatest stats are from today'
    nvalue = int(lvalue) + value
    response = stats.write_latest(nvalue)
    if response :
        print 'New value added to lastest file\nNow latest value :     %s' % nvalue
    else :
        print 'Problem while adding new value to latest'

""" we build the stats that will be displayed """
stat_o = stats.get_overall()
print '\nDOWNLOAD STATS\n'
print 'Current Month :      %s' % stats.pretty_display(stat_o['current_month'])
print 'Last 30 days :       %s' % stats.pretty_display(stat_o['last_30'])
print 'Current Week :       %s' % stats.pretty_display(stat_o['current_week'])
print 'Last 7 days :        %s' % stats.pretty_display(stat_o['last_7'])
