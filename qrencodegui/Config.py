#!/usr/bin/env python3

# config for qrencode-gui
import os

APP_NAME = 'qrencode-gui'
PREF = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share')
#PREF = '/usr/share'
GLADE = os.path.join(PREF, 'qrencodegui', 'qrencode-gui.glade')
