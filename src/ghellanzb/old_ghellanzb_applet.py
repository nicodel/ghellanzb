#!/usr/bin/env python

#
# ghellanzb applet
#

import pygtk, gtk, gnomeapplet, gobject, sys, gnome, pango, os, logging
pygtk.require('2.0')
from time import gmtime, strftime

# we import the required method to access hellanzb server
from xmlrpclib import ServerProxy

# we import the necessary hellanzb method to access configuration file and prettyEta
import Hellanzb, Hellanzb.PostProcessor
from Hellanzb.PostProcessorUtil import defineMusicType
from Hellanzb.Util import *
Hellanzb.SERVERS={}

# we add the modules path into the python path
PYTHON_DIR = '/usr/share/'
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

home_dir = os.getenv("HOME")
if os.listdir(home_dir).count('.ghellanzb') == 0:
    os.mkdir(home_dir + '/.ghellanzb')

from ghellanzb import name, version, ui_dir, images_dir, licence
import ghellanzb.ghellanzb_statistics as stats

# we create logger
logger = logging.getLogger('%s-%s' %(name, version))
logger.setLevel(logging.DEBUG)
# we create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s : %(message)s")
ch.setFormatter(formatter)
# we create a file handler and set the level to debug
#fh = logging.FileHandler(home_dir + '/ghellanzb.log')
fh = logging.handlers.RotatingFileHandler(filename=home_dir + '/ghellanzb.log', maxBytes=524288, backupCount=2)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
# add both handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

class ghellanzb_applet:
    def __init__(self, applet, iid):
        
        # we define some useful variables for ghellanzb_applet
        self.hella_status = ''
        self.status = ''
        self.info_label_data = ''
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.created_window = 0
        self.access = 0
        
        # we initiate the gnome application and set up internal variables
        gnome.init(name, version)

        # we define the applet
        self.applet = applet
        self.applet.connect('destroy', self.cleanup, None)       
        
        # We add the item in the right click menu
        ui_file = os.path.join(ui_dir, "GNOME_ghellanzb_applet.xml")
        verb_list = [("About", self.__display_about_dialog),
                     ("Statistics", stats.display_dialog)]
        self.applet.setup_menu_from_file(None, ui_file, name, verb_list)
        
        # We declare the tooltip
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self.applet, '%s - %s' % (name, version)) 
        
        # we create the frame to display the status label
        toolbar_frame = gtk.Frame()
        toolbar_event_box = gtk.EventBox()
        toolbar_event_box.add(toolbar_frame)
        toolbar_event_box.connect('button-press-event', self.applet_clicked)
        # we create the toolbar hbox that will receive icon
        self.toolbar_hbox = gtk.HBox(False, 0)
        toolbar_frame.add(self.toolbar_hbox)
        
        self.update_status()
        
        """
        # we create the toolbar applet label
        toolbar_label = gtk.Label('hellanzb : ')       
        # we create the toolbar applet status label
        self.toolbar_status = gtk.Label(self.status)
        # we add both labels to the toolbar box
        toolbar_hbox.add(toolbar_label)
        toolbar_hbox.add(self.toolbar_status)"""
        
        
        # we add the toolbar box to the applet
        self.applet.add(toolbar_event_box)
        
        self.applet.show_all()
        
        # we check the status of hellanzb every 5 seconds
        i = gobject.timeout_add(5000, self.update_status, self.applet)
        #print 'i is %s' % i        #DEBUG
    
    def cleanup(self, event, widget):
        del self.applet
    
    def update_status(self, event=None):
    
        try:
            self.get_status_from_server()
            logger.info('self.status is %s' % self.status)
            logger.info('self.access is %s' % self.access)
            if self.access == 1:
                self.extract_status()
        except:
            self.status = 'Unknown'
            self.access = 0
        
        # We empty the toolbar
        widget_list = self.toolbar_hbox.get_children()
        logger.info('Widget list : %s' % widget_list)
        if len(widget_list) != 0:
            for widget in widget_list:
                self.toolbar_hbox.remove(widget)
                logger.info('Removing widget : %s' % widget)
            
            
        if self.access != 0:
            if self.status == 'Nothing to do':
                icon_file = images_dir + '/ghellanzb_nothing_16.png'
                logger.info('Nothing to do')
            elif self.status == 'Downloading':
                icon_file = images_dir + '/ghellanzb_down_16.png'
                logger.info('Downloading')
            elif self.status == 'Processing':
                icon_file = images_dir + '/ghellanzb_proc_16.png'
                logger.info('Processing')
            elif self.status == 'Downloading and Processing':
                icon_file = images_dir + '/ghellanzb_down-proc_16.png'
                logger.info('Downloading and Processing')
        else:
            icon_file = images_dir + '/ghellanzb_error_16.png'
            logger.info(self.status)
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(icon_file)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.toolbar_hbox.add(image)
        self.toolbar_hbox.show_all()
        logger.info('Adding widget %s' % image)
        
        self.tooltips.set_tip(self.applet, '%s - %s\n%s' % (name, version, self.status)) 
        
        """self.toolbar_status.set_text(self.status)"""
        return True
    
    def applet_clicked(self, widget, event):
        #print 'button is %s' % event.button        #DEBUG
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            pass
            #print "let's display the menu"        #DEBUG
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
            #print "let's display the status"        #DEBUG
            if not self.window.props.visible:
                self.applet.set_state(gtk.STATE_SELECTED)
                if self.access == 0:
                    self.create_error_window()
                    self.position_window()
                    self.window.stick()
                    self.window.show_all()
                    self.window.grab_focus()
                else:
                    self.create_details_window()
                    self.position_window()
                    self.window.stick()
                    self.window.show_all()
                    self.window.grab_focus()
            else:
                self.applet.set_state(gtk.STATE_NORMAL)
                self.window.destroy()
            
    def create_details_window(self):
       
        self.window.set_decorated(False)
        self.window.set_resizable(False)
        self.window.set_keep_above(True)

        main_vbox = gtk.VBox(False, 0)
        self.window.add(main_vbox)
        
        
        # we build box and label to display info
        info_vbox = gtk.VBox(False, 0)
        info_vbox.set_border_width(6)
        main_vbox.add(info_vbox)
        version = self.hella_status['version']
        config_file = self.hella_status['config_file']
        info_1_label = gtk.Label('hellanzb v ' + version + ' - config file : ' + config_file)
        info_vbox.add(info_1_label)
        up_time = str(self.hella_status['uptime'])
        downloaded_nzbs = str(self.hella_status['total_dl_nzbs'])
        downloaded_files = str(self.hella_status['total_dl_files'])
        downloaded_segments = str(self.hella_status['total_dl_segments'])
        info_2_label = gtk.Label('up since : '  + up_time + '   downloaded  ' +  downloaded_nzbs + ' nzbs,  ' + downloaded_files + ' files,  ' + downloaded_segments + ' segments')
        info_vbox.add(info_2_label)
        
        # we build the box and frame to display the currently downloading
        if self.hella_status['rate'] == 0:
            cur_down_frame = gtk.Frame('Currently Downloading')
        else:
            cur_down_frame = gtk.Frame('Currently Downloading at %sKb/s' % self.hella_status['rate'])
        cur_down_frame.set_border_width(5)
        main_vbox.add(cur_down_frame)
        cur_down_vbox = gtk.VBox(False, 0)
        cur_down_vbox.set_border_width(6)
        #cur_down_frame.add(cur_down_vbox)
        cur_down_frame.add(cur_down_vbox)
        if len(self.hella_status['currently_downloading']) != 0:
            #print "something to download"        #DEBUG
            # we build the pair of labels to display nzb Name
            cur_down_name_hbox = gtk.HBox(False, 0)
            cur_down_name_label = gtk.Label('nzb Name :')
            cur_down_name_hbox.pack_start(cur_down_name_label, False, False, 5)
            cur_down_name_data = gtk.Label(self.hella_status['currently_downloading'][0]['nzbName'])
            cur_down_name_hbox.pack_end(cur_down_name_data, False, False, 5)
            cur_down_vbox.add(cur_down_name_hbox)
            # we build the pair of labels to display nzb size
            cur_down_size_hbox = gtk.HBox(False, 0)
            cur_down_size_label = gtk.Label('Size :')
            cur_down_size_hbox.pack_start(cur_down_size_label, False, False, 5)
            cur_down_size_data = gtk.Label(str(self.hella_status['currently_downloading'][0]['total_mb']) + 'MB')
            cur_down_size_hbox.pack_end(cur_down_size_data, False, False, 5)
            cur_down_vbox.add(cur_down_size_hbox)
            # we build the pair of labels to display time left
            cur_down_time_hbox = gtk.HBox(False, 0)
            cur_down_time_label = gtk.Label('Time Left :')
            cur_down_time_hbox.pack_start(cur_down_time_label, False, False, 5)
            cur_down_time_data = gtk.Label(prettyEta(self.hella_status['eta']))
            cur_down_time_hbox.pack_end(cur_down_time_data, False, False, 5)
            cur_down_vbox.add(cur_down_time_hbox)
            # we build the pair of labels to display percentage completed
            cur_down_completed_hbox = gtk.HBox(False, 0)
            cur_down_completed_label = gtk.Label('Percentage Completed :')
            cur_down_completed_hbox.pack_start(cur_down_completed_label, False, False, 5)
            cur_down_completed_data = gtk.Label(str(self.hella_status['percent_complete']) + '%')
            cur_down_completed_hbox.pack_end(cur_down_completed_data, False, False, 5)
            cur_down_vbox.add(cur_down_completed_hbox)
        else:
            #print "nothing to download"        #DEBUG
            # we build the label to display None
            cur_down_name_hbox = gtk.HBox(False, 0)
            cur_down_name_label = gtk.Label('None')
            cur_down_name_hbox.pack_start(cur_down_name_label, False, False, 5)
            cur_down_vbox.add(cur_down_name_hbox)
        
        # we build the box and frame to display the queue
        queued_frame = gtk.Frame('Queue')
        queued_frame.set_border_width(5)
        main_vbox.add(queued_frame)
        queued_vbox = gtk.VBox(False, 0)
        queued_vbox.set_border_width(6)
        #queued_frame.add(queued_vbox)
        queued_frame.add(queued_vbox)
        if len(self.hella_status['queued']) != 0:
            # we build the label to display name and size of each queued nzb
            for queued_nzb in self.hella_status['queued']:
                #print 'queued_nzb is %s' % queued_nzb        #DEBUG
                queued_hbox = gtk.HBox(False, 0)
                queued_vbox.add(queued_hbox)
                # we build the nzb name labels pair
                queued_name_hbox = gtk.HBox(False, 0)
                queued_name_label = gtk.Label('nzb Name :')
                queued_name_hbox.pack_start(queued_name_label, False, False, 5)
                queued_name_data = gtk.Label(queued_nzb['nzbName'])
                queued_name_hbox.pack_start(queued_name_data, False, False, 5)
                queued_hbox.add(queued_name_hbox)
                # we build the nzb size labels pair
                queued_size_hbox = gtk.HBox(False, 0)
                try:
                    queued_size_data = gtk.Label(str(queued_nzb['total_mb']) + 'MB')
                except:
                    queued_size_data = gtk.Label('N/A')
                queued_size_hbox.pack_end(queued_size_data, False, False, 5)
                queued_size_label = gtk.Label('Size :')
                queued_size_hbox.pack_end(queued_size_label, False, False, 5)
                queued_hbox.add(queued_size_hbox)
        else :
            # we build the label to display None
            queued_name_hbox = gtk.HBox(False, 0)
            queued_name_label = gtk.Label('None')
            queued_name_hbox.pack_start(queued_name_label, False, False, 5)
            queued_vbox.add(queued_name_hbox)
        
        # we build the box and frame to display the currently processing
        proces_frame = gtk.Frame('Currently Processing')
        proces_frame.set_border_width(5)
        main_vbox.add(proces_frame)
        proces_vbox = gtk.VBox(False, 0)
        proces_vbox.set_border_width(6)
        proces_frame.add(proces_vbox)
        if len(self.hella_status['currently_processing']) != 0: 
            logger.debug("self.hella_status['currently_processing'] is : %s" % self.hella_status['currently_processing'])
            # we build the label to display name of currently processing nzb
            proces_name_hbox = gtk.HBox(False, 0)
            proces_name_label = gtk.Label(self.hella_status['currently_processing'][0]['nzbName'])
            proces_name_hbox.pack_start(proces_name_label, False, False, 5)
            proces_vbox.add(proces_name_hbox)
        else :
            # we build the label to display None
            proces_name_hbox = gtk.HBox(False, 0)
            proces_name_label = gtk.Label('None')
            proces_name_hbox.pack_start(proces_name_label, False, False, 5)
            proces_vbox.add(proces_name_hbox)
        
        
        
        
        # we build the box and frame to display the logs
        logs_frame = gtk.Frame('Logs')
        logs_frame.set_border_width(5)
        main_vbox.add(logs_frame)
        logs_vbox = gtk.VBox(False, 0)
        logs_vbox.set_border_width(6)
        #logs_frame.add(logs_vbox)
        logs_frame.add(logs_vbox)
        for logs in self.hella_status['log_entries']:
            log_hbox = gtk.HBox(False, 0)
            try: 
                len(logs['INFO'])
                log_label = gtk.Label(logs['INFO'])
            except: 
                pass
            try: 
                len(logs['ERROR'])
                log_label = gtk.Label(logs['ERROR'])
            except: 
                pass
            try: 
                len(logs['WARN'])
                log_label = gtk.Label(logs['WARN'])
            except: 
                pass
            try: 
                len(logs['WARNING'])
                log_label = gtk.Label(logs['WARNING'])
            except: 
                pass
            log_hbox.pack_start(log_label, False, False, 5)
            logs_vbox.add(log_hbox)        
        
        # we tell the rest of the code that the window has been already created
        self.created_window = 1
        
    def create_error_window(self):
        
        file_path = '/etc/hellanzb.conf'
        execfile(file_path)
        
        self.window.set_decorated(False)
        self.window.set_resizable(False)
        self.window.set_keep_above(True)

        main_vbox = gtk.VBox(False, 6)
        self.window.add(main_vbox)
        
        error_frame = gtk.Frame(self.status)
        main_vbox.add(error_frame)
        
        error_vbox = gtk.VBox(False, 0)
        error_vbox.set_border_width(6)
        error_frame.add(error_vbox)
        
        hellanzb_generic_message = """
        For more information regarding hellanzb configuration, please refer to the following web page :
        http://www.hellanzb.com/trac/
        """

        server_error_message = """
        gHellanzb was not able to retreive the XMLRPC server configured in the hellanzb configuration file (%s).
        Please check that the following variable is not commented in the above file and that it refers to a IP address:
        XMLRPC_SERVER
        
        %s    
        """ % (file_path, hellanzb_generic_message)
        
        port_error_message ="""
        gHellanzb was not able to retreive the XMLRPC port configured in the hellanzb configuration file (%s).
        Please check that the following variable is not commented in the above file and that it refers to a proper port number:
        XMLRPC_PORT
        
        %s 
        """ % (file_path, hellanzb_generic_message)
        
        password_error_message ="""
        gHellanzb was not able to retreive the XMLRPC password configured in the hellanzb configuration file (%s).
        Please check that the following variable is not commented in the above file and that it refers to a proper password:
        XMLRPC_PASSWORD
        
        %s 
        """ % (file_path, hellanzb_generic_message)
        
        unknown_error_message = """
        OK, for this one I don't know.
        
        %s
        """ % hellanzb_generic_message
        
        config_file_error_message = """
        gHellanzb was not able to locate hellanzb configuration file. Its default location should be :
        %s
        """ % file_path
        
        if self.status == 'not reachable':
            access_error_message = """
            gHellanzb was not able to reach the XMLRPC server configured in the hellanzb configuration file (%s):
            XMLRPC_SERVER : %s
            XMLRPC_PORT : %s
            XMLRPC_PASSWORD :%s
            Please check that hellanzb is actually running using the following command in a terminal for example : ps -aef |grep hellanzb.
            
            %s
            """ % (file_path,
                   str(getattr(Hellanzb, 'XMLRPC_SERVER')),
                   str(getattr(Hellanzb, 'XMLRPC_PORT')),
                   str(getattr(Hellanzb, 'XMLRPC_PASSWORD')),
                   hellanzb_generic_message
                   )
            error_label = gtk.Label(access_error_message)
        if self.status == 'no xmlrpc server configured':
            error_label = gtk.Label(server_error_message)
        if self.status == 'no xmlrpc port configured':
            error_label = gtk.Label(port_error_message)
        if self.status == 'no xmlrpc password configured':
            error_label = gtk.Label(password_error_message)
        if self.status == 'config file not found':
            error_label = gtk.Label(config_file_error_message)
        
        
        error_vbox.pack_start(error_label, False, False, 5)
        
        # we tell the rest of the code that the window has been already created
        self.created_window = 1 
        
    def position_window(self):
        #
        # this method is from ontv application
        #
        
        self.window.realize()
        gtk.gdk.flush()

        (w, h) = self.window.get_size()
        (w, h) = self.window.size_request()

        (x, y, gravity) = self.get_docking_data(False, w, h)

        self.window.move(x, y)
        self.window.set_gravity(gravity)
    
    def get_docking_data(self, middle, w=0, h=0):
        #
        # this method is from ontv application
        #
        
        self.applet.realize()
        (x, y) = self.applet.window.get_origin()

        button_w = self.applet.allocation.width
        button_h = self.applet.allocation.height

        screen = self.applet.get_screen()

        found_monitor = False
        n = screen.get_n_monitors()
        for i in range(0, n):
            monitor = screen.get_monitor_geometry(i)
            if (x >= monitor.x and x <= monitor.x + monitor.width and
                y >= monitor.y and y <= monitor.y + monitor.height):
                    found_monitor = True
                    break

        if not found_monitor:
            screen_width = screen.get_width()
            monitor = gtk.gdk.Rectangle(0, 0, screen_width, screen_width)

        orient = self.applet.get_orient()

        if orient == gnomeapplet.ORIENT_RIGHT:
            x += button_w

            if ((y + h) > monitor.y + monitor.height):
                y -= (y + h) - (monitor.y + monitor.height)

            if middle:
                x -= button_w/2
                y += button_h/2

            if ((y + h) > (monitor.height / 2)):
                gravity = gtk.gdk.GRAVITY_SOUTH_WEST
            else:
                gravity = gtk.gdk.GRAVITY_NORTH_WEST
        elif orient == gnomeapplet.ORIENT_LEFT:
            x -= w

            if ((y + h) > monitor.y + monitor.height):
                y -= (y + h) - (monitor.y + monitor.height)

            if middle:
                x += w/2
                y += button_h/2

            if ((y + h) > (monitor.height / 2)):
                gravity = gtk.gdk.GRAVITY_SOUTH_EAST
            else:
                gravity = gtk.gdk.GRAVITY_NORTH_EAST
        elif orient == gnomeapplet.ORIENT_DOWN or self.config.standalone:
            y += button_h

            if ((x + w) > monitor.x + monitor.width):
                x -= (x + w) - (monitor.x + monitor.width)

            if middle:
                x += button_w/2
                y -= button_h/2

            gravity = gtk.gdk.GRAVITY_NORTH_WEST
        elif orient == gnomeapplet.ORIENT_UP:
            y -= h

            if ((x + w) > monitor.x + monitor.width):
                x -= (x + w) - (monitor.x + monitor.width)

            if middle:
                x += button_w/2
                y += h/2

            gravity = gtk.gdk.GRAVITY_SOUTH_WEST

        return (x, y, gravity)
         
        
    def get_status_from_server(self):
        """
        conf_dir_list = os.listdir('/usr/etc/')
        if conf_dir_list.count('hellanzb.conf') == 0:
            conf_dir_list = os.listdir('/etc/')
            if conf_dir_list.count('hellanzb.conf') == 0:
                self.status = 'conf file not found'
                self.access = 0
                print self.status
                return
            else:
                file_path = '/etc/hellanzb.conf'
                self.access = 1
                print 'file_path is : %s' % file_path
                return
        else:
            file_path = '/usr/etc/hellanzb.conf'
            print 'file_path is : %s' % file_path
            self.access = 1
            return
        """
        file_path = '/etc/hellanzb.conf'
        try:
            execfile(file_path)
        except:
            self.status = 'conf file not found'
            self.access = 0
            #print self.status
            return
        # we extract the necessary variables from the configuration file
        try:
            server = str(getattr(Hellanzb, 'XMLRPC_SERVER'))
        except:
            self.status = 'no xmlrpc server configured'
            self.access = 0
            #print self.status
            return
        try:
            port = str(getattr(Hellanzb, 'XMLRPC_PORT'))
        except:
            self.status = 'no xmlrpc port configured'
            self.access = 0
            #print self.status
            return
        try:
            server_password = str(getattr(Hellanzb, 'XMLRPC_PASSWORD'))
        except:
            self.status = 'no xmlrpc password configured'
            self.access = 0
            #print self.status
            return
        
        # we build the hellanzb access url
        hella_server = ServerProxy('http://' + 'hellanzb' + ':' + server_password + '@' + server + ':' + port)
        
        # we get hellanzb status
        try:
            self.hella_status = hella_server.status()
        except:
            self.status = 'not reachable'
            self.access = 0
            #print self.status
            return
        # if we get there everything is fine
        self.access = 1
        
    def extract_status(self):
        if len(self.hella_status['currently_downloading']) == 0 and len(self.hella_status['currently_processing']) == 0:
            self.status = 'Nothing to do'
            #print self.status        #DEBUG
        elif len(self.hella_status['currently_downloading']) != 0 and len(self.hella_status['currently_processing']) == 0:
            self.status = 'Downloading'
            #print self.status        #DEBUG
        elif len(self.hella_status['currently_downloading']) == 0 and len(self.hella_status['currently_processing']) != 0:
            self.status = 'Processing'
            #print self.status        #DEBUG
        elif len(self.hella_status['currently_downloading']) != 0 and len(self.hella_status['currently_processing']) != 0:
            self.status = 'Downloading and Processing'
    
    def __display_about_dialog(self, uicomponent=None, verb=None):
        self.window = gtk.AboutDialog()
        self.window.set_name(name)
        self.window.set_version(version)
        #self.window.set_authors(['%s    %s' % (author, author_mail)])
        self.window.set_authors([open('/usr/doc/share/ghellanzb/CREDITS','r').read()])
        logo = gtk.gdk.pixbuf_new_from_file(images_dir + '/ghellanzb_logo_48.png')
        self.window.set_logo(logo)
        
        self.window.set_copyright(licence)
        self.window.set_position(gtk.WIN_POS_CENTER)
        
        self.window.connect("destroy", self.hide, self.window)
        self.window.run()
        self.window.destroy()
        return
    
    def hide(self, widget, event):
        #print "Let's hide this window"
        widget.hide()
        return
    
    
    
    
def create_factory(applet, iid):
    ghellanzb_applet(applet, iid)
    return True

if len(sys.argv) == 2 and sys.argv[1] == "--window":
    #print 'ok we do something'    #DEBUG
    window = gtk.Window()
    window.set_title('hellanzb applet')
    window.connect('destroy', gtk.main_quit)
    app = gnomeapplet.Applet()
    create_factory(app, None)
    app.reparent(window)
    window.show_all()
    gtk.main()
    sys.exit()
    
logger.info("Starting factory")
gnomeapplet.bonobo_factory("OAFIID:GNOME_ghellanzb_applet_Factory", gnomeapplet.Applet.__gtype__, "ghellanzb", version, create_factory)

logger.info("Factory ended")
 
