#!/usr/bin/env python

#
# ghellanzb statistics
#

import os, simplejson, re
from time import gmtime, strftime
from datetime import timedelta, datetime

import ghellanzb
home_dir = os.getenv("HOME") + '/.ghellanzb'
#home_dir = '../tmp/ghellanzb'    # DEV MODE

"""
The statistics directory will be something like :
~/.ghellanzb/statistics/all.stats
~/.ghellanzb/statistics/last.stats
    all.stats : ['2009':['01':['01':xxx], ['02':xx], ...
    last.stats :20090209 13:45 xxx
    
    where xxx is the value of 'total_mb' extracted for the hellanzb status.

"""
current_year_dir = strftime('%Y')
current_month_file = '%s.stats' % strftime('%m')

if os.listdir(home_dir).count('statistics') == 0:
    os.mkdir(home_dir + '/statistics')
if os.listdir(home_dir + '/statistics').count('all.stats') == 0:
    f = open(home_dir + '/statistics/all.stats', 'w')
    f.close()
if os.listdir(home_dir + '/statistics').count('last.stats') == 0:
    f = open(home_dir + '/statistics/last.stats', 'w')
    f.close()
    
latest_file = home_dir + '/statistics/last.stats'
stats_file = home_dir + '/statistics/all.stats'
now = strftime('%Y%m%d %H:%M')

def write_latest(value):
    try:
        f = open(latest_file, 'w')
        f.write ('%s %s' % (now, str(value)))
        f.close()
        return True
    except:
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
        stats = simplejson.load(open(stats_file, 'r'))
        if not stats.has_key(date.strftime('%Y')):
            stats[date.strftime('%Y')] = {}
        if not stats[date.strftime('%Y')].has_key(date.strftime('%m')):
            stats[date.strftime('%Y')][date.strftime('%m')] = {}
        if not stats[date.strftime('%Y')][date.strftime('%m')].has_key(date.strftime('%d')):
            stats[date.strftime('%Y')][date.strftime('%m')][date.strftime('%d')] = []
        stat = random.randint(300,4550)
        stats[date.strftime('%Y')][date.strftime('%m')][date.strftime('%d')] = stat
        return True
    except:
        return False
    
def add_new_day(date, value):
    try:
        stats = simplejson.load(open(stats_file, 'r'))
        stats[date[0:4]][date[4:6]][date[6:8]] = value
        f = open(stats_file, 'w')
        simplejson.dump(stats, f)
        f.close()
        return True
    except:
        return False

    
def get_overall():
    overall_stats = {}
    stats = simplejson.load(open(stats_file, 'r'))
    # we build the current month stats
    cm_stat = 0
    for day in stats[strftime('%Y')][strftime('%m')].keys():
        cm_stat = int(cm_stat) + int(stats[strftime('%Y')][strftime('%m')][day])
    overall_stats['current_month'] = cm_stat
    
    # we build the last 30 days stats
    last_30_stat = 0
    day = datetime.today() - timedelta(days=1)
    print 'day      %s' % day
    print 'last     %s' % (datetime.today() - timedelta(days=30))
    while day.strftime('%Y%m%d') != (datetime.today() - timedelta(days=30)).strftime('%Y%m%d') :
        if stats[day.strftime('%Y')][day.strftime('%m')].has_key(day.strftime('%d')):
            last_30_stat = int(last_30_stat) + int(stats[day.strftime('%Y')][day.strftime('%m')][day.strftime('%d')])
        else:
            pass
        day = day - timedelta(days=1)
    overall_stats['last_30'] = last_30_stat

    # we build the current week stats
    cw_stat = 0
    day = datetime.today() - timedelta(days=1)
    wday = day.weekday()
    while wday != -1:
        if stats[day.strftime('%Y')][day.strftime('%m')].has_key(day.strftime('%d')):
            cw_stat = int(cw_stat) + int(stats[day.strftime('%Y')][day.strftime('%m')][day.strftime('%d')])
        else:
            pass
        day = day - timedelta(days=1)
        wday = wday - 1
    overall_stats['current_week'] = cw_stat
    
    # we uild the last 7 days stats
    last_7_stat = 0
    day = datetime.today() - timedelta(days=1)
    while day != (datetime.today() - timedelta(days=7)):
        if stats[day.strftime('%Y')][day.strftime('%m')].has_key(day.strftime('%d')):
            last_7_stat = int(last_7_stat) + int(stats[day.strftime('%Y')][day.strftime('%m')][day.strftime('%d')])
        else:
            pass
        day = day - timedelta(days=1)
    overall_stats['last_7'] = last_7_stat
    return overall_stats

def split_thousands(s, t_sep, d_dep=None):
    if s.rfind('.')>0:
        rhs=s[s.rfind('.')+1:]
        s=s[:s.rfind('.')-1]
        if len(s) <= 3: return s + d_dep + rhs
        return split_thousands(s[:-3], t_sep) + d_dep + s[-3:] + d_dep + rhs
    else:
        if len(s) <= 3: return s
        return split_thousands(s[:-3], t_sep) + t_sep + s[-3:]


def pretty_display(value):
    value = split_thousands(str(value), ' ')
    return '%s MB'% value

def display_dialog(stats):
    print 'display stats dialog'
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("Statistics")
    window.set_border_width(2)
    window.set_position(gtk.WIN_POS_CENTER)
    window.connect("destroy", destroy, window)
    
    VBox = gtk.VBox()
    window.add(VBox)
    Vbox.set_border_width(6)
    
    week_frame = gtk.Frame()
    week_frame.set_border_width(5)
    VBox.add(week_frame)
    week_vbox = gtk.VBox(False, 0)
    week_vbox.set_border_width(6)
    week_frame.add(week_vbox)
    box = build_label_value_pair('Current Week',pretty_display(stats['current_week']))
    week_vbox.add(box)
    box = build_label_value_pair('Last 7 days',pretty_display(stats['last_7']))
    week_vbox.add(box)
    
    month_frame = gtk.Frame()
    month_frame.set_border_width(5)
    VBox.add(month_frame)
    month_vbox = gtk.VBox(False, 0)
    month_vbox.set_border_width(6)
    month_frame.add(month_vbox)
    box = build_label_value_pair('Current Month',pretty_display(stats['current_month']))
    week_vbox.add(box)
    box = build_label_value_pair('Last 30 days',pretty_display(stats['last_30']))
    week_vbox.add(box)
    
def build_label_value_pair(label, value):
    box =gtk.HBox(False,0)
    w_label = gtk.Label(label)
    box.pack_start(w_labelFalse, False, False, 5)
    w_nb = gtk.Label(value)
    box.pack_end(w_nb, False, False, 5)
    return box
    
    
    
    return
def destroy(widget, event):
    widget.destroy()
