#!/usr/bin/env python

#
# ghellanzb statistics
#

import os, simplejson
from time import gmtime, strftime
from datetime import timedelta, datetime

#import ghellanzb
#home_dir = os.getenv("HOME") + '/.ghellanzb'
home_dir = '../tmp/ghellanzb'    # DEV MODE

"""
The statistics directory will be something like :
~/.ghellanzb/statistics/2009/01.stats
~/.ghellanzb/statistics/last.stats
    01.stats : [[1,xxx],[2,xxx], ...]
    last.stats :20090209 13:45 xxx
    
    where xxx is the value of 'total_mb' extracted for the hellanzb status.

"""
current_year_dir = strftime('%Y')
current_month_file = '%s.stats' % strftime('%m')



if os.listdir(home_dir).count('statistics') == 0:
    os.mkdir(home_dir + '/statistics')
if os.listdir(home_dir + '/statistics/').count(strftime('%Y')) == 0:
    os.mkdir(home_dir + '/statistics/%s' % strftime('%Y'))
if os.listdir(home_dir + '/statistics/%s' % current_year_dir).count(current_month_file) == 0:
    f = open(home_dir + '/statistics/%s/%s' % (current_year_dir, current_month_file), 'w')
    f.close()
if os.listdir(home_dir + '/statistics').count('last.stats') == 0:
    f = open(home_dir + '/statistics/last.stats', 'w')
    f.close()
    
latest_file = home_dir + '/statistics/last.stats'
current_month_file = home_dir + '/statistics/%s/%s' % (current_year_dir,current_month_file)
now = strftime('%Y%m%d %H:%M')
'''
month = []
month.append(('1','555'))
month.append(('2','444'))
month.append(('3','777'))
f = open(current_month_file, 'w')
simplejson.dump(month, f)
f.close()
'''
def write_latest(value):
    try:
        f = open(latest_file, 'w')
        f.write ('%s %s' % (now, str(value)))
        f.close()
        print 'write successful'
    except:
        print 'write failed'
        return False
    

def get_latest():
    f = open(latest_file, 'r')
    t = f.read()
    date = t[:14]
    value = t[15:]
    f.close()
    return date, value
    
def write_to_disk(date, value):
    try:
        f = open(current_month_file, 'r')
        monthly = simplejson.load(f)
        f.close()
        monthly.append((date[6:], value))
        f = open(current_month_file, 'w')
        simplejson.dump(monthly, f)
        f.close()
        return True
    except:
        return False
    
def get_overall():
    overall_stats = {}
    """ we build the current month stats """
    print '\nBuilding current month'
    current_month = simplejson.load(open(current_month_file, 'r'))
    #d = len(current_month)
    cm_stat = 0
    for day in current_month:
        cm_stat = int(day[1]) + cm_stat
    overall_stats['current_month'] = cm_stat
    
    # we build the last 30 days stats
    t = 30
    day = datetime.today()
    delta = timedelta(days=1)
    last_30_stat = 0
    m = int(strftime('%m'))
    m = m -1
    if m < 10:
        m = '0%s' % m
    last_month_file = '%s.stats' % m
    last_month_dir = home_dir + '/statistics/%s/%s' % (current_year_dir,last_month_file)
    last_month = simplejson.load(open(last_month_dir, 'r'))
    print '\n'
    while t != 0:
        print day
        for day in current_month:
            if t_day == int(day[0]):
                last_30_stat = int(day[1]) + last_30_stat
        day = day - delta
        t = t - 1

    overall_stats['last_30'] = last_30_stat
        
    
    
    return overall_stats
