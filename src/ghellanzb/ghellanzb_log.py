#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# 
# ghellanzb
#
#
# Released under the GNU General Public License
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
# Module used to manage the logger
#

import os, logging
import logging.handlers

home_dir = os.getenv("HOME")

# we create logger and its formatter
logger = logging.getLogger('ghellanzb')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s%(message)s")
# we create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# we create a file handler and set the level to info
#fh = logging.FileHandler(home_dir + '/.ghellanzb/ghellanzb.log')
fh = logging.handlers.RotatingFileHandler(filename=home_dir + '/.ghellanzb/ghellanzb.log', maxBytes=524288, backupCount=3)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
# add both handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)