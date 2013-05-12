#!/usr/bin/env python3

# config for qrencode-gui
#import gettext
#from gettext import gettext as _
import os

APP_NAME = 'qrencode-gui'
PREF = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share')
#PREF = '/usr/share'
LOCALEDIR = os.path.join(PREF, 'locale')
GLADE = os.path.join(PREF, 'qrencodegui', 'qrencode-gui.glade')

#gettext.bindtextdomain('qrencode-gui', LOCALEDIR)
#gettext.textdomain('qrencode-gui')
