#!/usr/bin/env python3

import os
import json

PREF = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share')
#PREF = '/usr/share'

_files = ('qrencode-about.glade', 
          'qrencode-addr.glade',
          'qrencode-cal.glade',
          'qrencode-email.glade',
          'qrencode-geo.glade',
          'qrencode-gui.glade',
          'qrencode-phone.glade',
          'qrencode-sms.glade',
          'qrencode-text.glade',
          'qrencode-wifi.glade',
          )
GLADE_FILES = [os.path.join(PREF, 'qrencodegui', glade) for glade in _files]
HOME_DIR = os.path.expanduser('~')
_conf_file = os.path.join(HOME_DIR, '.config', 'qrencodegui', 'conf.json')
_default_conf = {
        'bg': 'rgba(255, 255, 255, 1.0)',
        'fg': 'rgba(0, 0, 0, 1.0)',
        'size': 6,
        'margin': 3,
        'error': 0,
        }

def load_conf():
    if os.path.exists(_conf_file):
        with open(_conf_file) as fh:
            return json.loads(fh.read())
    else:
        try:
            os.makedirs(os.path.dirname(_conf_file))
        except OSError as e:
            print(e)
        dump_conf(_default_conf)
        return _default_conf

def dump_conf(conf):
    with open(_conf_file, 'w') as fh:
        fh.write(json.dumps(conf))
