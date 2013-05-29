#!/usr/bin/env python

#
# python ghellanzb statistics module
#

import ghellanzb_statistics as stats
from time import gmtime, strftime


stats = stats.get_overall()
print '\nDOWNLOAD STATS\n'
print 'Current Month :      %s' % stats['current_month']
print 'Last 30 days :       %s' % stats['last_30']
print 'Current Week :       %s' % stats['current_week']