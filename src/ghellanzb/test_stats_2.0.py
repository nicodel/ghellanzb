#!/usr/bin/env python

#
# python ghellanzb statistics module
#

import ghellanzb_statistics as stats
from time import gmtime, strftime
from datetime import timedelta, datetime

def get_weekday_name(nb):
    if nb == 0:
        day = 'Monday'
    if nb == 1:
        day = 'Tuesday'
    if nb == 2:
        day = 'Wednesday'
    if nb == 3:
        day = 'Thrusday'
    if nb == 4:
        day = 'Friday'
    if nb == 5:
        day = 'Saturday'
    if nb == 6:
        day = 'Sunday'
    return day

today = datetime.today()

day_offset = timedelta(days=1)
print 'today :      %s' % today

tomorrow = today + day_offset
print 'tomorrow :   %s' % tomorrow

yesterday = today - day_offset
print 'yesterday :  %s' % yesterday

week_day = today.weekday()
print 'Week day is :    %s (%s)' % (week_day, get_weekday_name(week_day))






