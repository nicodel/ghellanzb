#!/usr/bin/env python

# 
# ghellanzb applet
#

from distutils.core import setup
import ghellanzb

# Put this here, so we can overwrite it in build.py
version = ghellanzb.version
name = ghellanzb.name

def runSetup():
    options = dict(
        name = name,
        version = version,
        author = 'Nicolas Delebecque',
        author_email = '<nicolas.delebecque@gmail.com>',
        url = 'http://nicoworkspace.free.fr/?q=ghellanzb-downloads',
        license = 'GNU/GPL',
        platforms = ['unix'],
        description = 'gnome applet monitoring hellanzb',
        long_description = ("ghellanzb is a small gnome applet monitoring hellanzb"),

        packages = ['ghellanzb'],
        scripts = ['ghellanzb/ghellanzb_applet.py'],
        data_files = [('lib/bonobo/servers', ['servers/GNOME_ghellanzb_applet.server' ]),
                       ('share/doc/ghellanzb', ['CHANGELOG', 'CREDITS', 'README' , 'PKG-INFO' ])],
        )

    setup(**options)

if __name__ == '__main__':
    runSetup()
