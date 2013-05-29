#!/usr/bin/env python

#
# ghellanzb launcher
#

import sys, getopt, os, gnome, gnomeapplet, gtk, shutil


# we add the modules path into the python path
PYTHON_DIR = '/usr/share/'
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

home_dir = os.getenv("HOME")

from ghellanzb import name, version
from ghellanzb.ghellanzb_applet import ghellanzb_applet
import ghellanzb.ghellanzb_log as log

def main():
    """
    Module used to start the gnome applet
    """
    
    # We declare and check the possible options that can be add the command
    window_mode = False
    debug = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cdhw", ["configure", "debug", "help", "window"])
    except getopt.GetoptError:
        opts = []
        args = sys.argv[1:]
    for o, a in opts:
        if o in ("-w", "--window"):
            window_mode = True
        if o in ("-d", "--debug"):
            window_mode = True
            debug = True
    
    # We check if all the necessary files and directories are here
    # Home directory (will contain all the sub-directories and files)
    if os.listdir(home_dir).count('.ghellanzb') == 0:
        os.mkdir(home_dir + '/.ghellanzb')

    # We initiate the gnome applet and the threads
    gnome.init(name, version)
    gtk.gdk.threads_init()

    if window_mode:
        # We build the window and launch it
        #log.logger.info("_launcher : Starting in Window Mode")
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title(name)
        window.props.allow_grow = False
        window.connect("destroy", gtk.main_quit)
        applet = gnomeapplet.Applet()
        if debug :
            applet_factory(applet, None, True, True)
        else :
            applet_factory(applet, None, True, False)
        applet.reparent(window)
        window.show_all()
        gtk.main()
    else:
        # We activate the bonobo factory
        activate_factory(window_mode=False)


def applet_factory(applet, iid=None, window_mode=False, debug=False):
    """
    Module used to start the gnome applet
    """
    g_applet = ghellanzb_applet(applet, window_mode, debug)
    return True

def activate_factory(window_mode=False):
    """
    Module used to activate the bonobo factory
    """
    #log.logger.info(" ##########################################")
    #log.logger.info(" : Starting Factory")
    #log.logger.info(" ##########################################")
    gnomeapplet.bonobo_factory("OAFIID:GNOME_ghellanzb_applet_Factory",
                               gnomeapplet.Applet.__gtype__, 
                               name, 
                               version,
                               applet_factory, window_mode)
    #log.logger.info(" ##########################################")
    #log.logger.info("_launcher : Factory Ended")
    #log.logger.info(" ##########################################\n")
    
if __name__ == "__main__":
    main()
