#!/usr/bin/env python


from time import gmtime, strftime
from datetime import timedelta, datetime
import random, simplejson

date = datetime.today() - timedelta(days=180)
print 'Start date is :      %s\n' % date

stats = {}

while date.strftime('%Y%m%d') != datetime.today().strftime('%Y%m%d'):
    if not stats.has_key(date.strftime('%Y')):
        stats[date.strftime('%Y')] = {}
    if not stats[date.strftime('%Y')].has_key(date.strftime('%m')):
        stats[date.strftime('%Y')][date.strftime('%m')] = {}
    if not stats[date.strftime('%Y')][date.strftime('%m')].has_key(date.strftime('%d')):
        stats[date.strftime('%Y')][date.strftime('%m')][date.strftime('%d')] = []
    stat = random.randint(300,4550)
    stats[date.strftime('%Y')][date.strftime('%m')][date.strftime('%d')] = stat
    print '%s       %s' % (date, stat)
    
    date = date + timedelta(days=1)

file = '../tmp/ghellanzb/statistics/all.stats'
f = open(file, 'w')
simplejson.dump(stats, f)
f.close()