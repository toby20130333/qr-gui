
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import os
import json

if __file__.startswith('/usr/local/'):
    PREF = '/usr/local/share'
elif __file__.startswith('/usr/'):
    PREF = '/usr/share'
else:
    PREF = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share')

APPNAME = 'QR GUI'
VERSION = '3.0.1'
HOMEPAGE = 'https://github.com/LiuLang/qr-gui'
AUTHORS = ['LiuLang <gsushzhsosgsu@gmail.com>',]
DESCRIPTION = 'QR encode / decode tool for Linux users'

HOME_DIR = os.path.expanduser('~')
CONF_DIR = os.path.join(HOME_DIR, '.config', 'qr-gui')
_conf_file = os.path.join(CONF_DIR, 'conf.json')
_default_conf = {
        'bg': 'rgba(255, 255, 255, 1.0)',
        'fg': 'rgba(0, 0, 0, 1.0)',
        'pixel': 6,    # pixel size
        'margin': 3,   # margin size
        'error': 0,    # error correction level
        'window-size': (1000, 650)
        }

def load_conf():
    if os.path.exists(_conf_file):
        with open(_conf_file) as fh:
            return json.loads(fh.read())
    else:
        if not os.path.exists(CONF_DIR):
            os.makedirs(CONF_DIR)
        dump_conf(_default_conf)
        return _default_conf

def dump_conf(conf):
    with open(_conf_file, 'w') as fh:
        fh.write(json.dumps(conf))
