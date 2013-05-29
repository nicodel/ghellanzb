#!/usr/bin/env python

from py2deb import Py2deb
import ghellanzb

changelog=open('doc/CHANGELOG','r').read()

p = Py2deb(ghellanzb.unix_name)
p.depends = 'python-gtk2, python, hellanzb'
p.url = ghellanzb.homepage
p.author = ghellanzb.author
p.mail = ghellanzb.author_mail
p.description = ghellanzb.description
p.licence = ghellanzb.licence
p.arch = 'i386'

p['/usr/share'] = ['ghellanzb/__init__.py',
                   'ghellanzb/ghellanzb_applet.py',
                   'ghellanzb/ghellanzb_statistics.py',
                   'ghellanzb/ghellanzb_log.py',
                   'images/ghellanzb_logo_48.png|ghellanzb/images/ghellanzb_logo_48.png',
                   'images/ghellanzb_nothing_16.png|ghellanzb/images/ghellanzb_nothing_16.png',
                   'images/ghellanzb_down_16.png|ghellanzb/images/ghellanzb_down_16.png',
                   'images/ghellanzb_proc_16.png|ghellanzb/images/ghellanzb_proc_16.png',
                   'images/ghellanzb_error_16.png|ghellanzb/images/ghellanzb_error_16.png',
                   'images/ghellanzb_down-proc_16.png|ghellanzb/images/ghellanzb_down-proc_16.png']

p['/usr/bin'] = ['ghellanzb/ghellanzb_launcher.py|ghellanzb']
p['/usr/share/gnome-2.0'] = ['ui/GNOME_ghellanzb_applet.xml']
p['/usr/lib/bonobo'] = ['servers/GNOME_ghellanzb_applet.server']
p['/usr/doc/share/ghellanzb'] = ['doc/CHANGELOG|CHANGELOG',
                                 'doc/CREDITS|CREDITS', 
                                 'doc/README|README' , 
                                 'doc/PKG-INFO|PKG-INFO']

p.generate(ghellanzb.version, changelog, src = True)
