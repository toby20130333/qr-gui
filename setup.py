#!/usr/bin/env python3

# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in the LICENSE file.

from distutils.core import setup
from distutils.core import Command
from distutils.command.clean import clean as distutils_clean
from distutils.command.sdist import sdist as distutils_sdist
import glob
import os
import shutil

from qr_gui import Config

def build_data_files():
    data_files = []
    for dir, dirs, files in os.walk('share'):
        #target = os.path.join('share', dir)
        target = dir
        if files:
            files = [os.path.join(dir, f) for f in files]
            data_files.append((target, files))
    return data_files

# will be installed to /usr/local/bin
scripts = ['qr-gui', ]

if __name__ == '__main__':
    setup(
        name = 'qr-gui',
        description = Config.DESCRIPTION,
        version = Config.VERSION,
        license = 'GPLv3',
        url = Config.HOMEPAGE,

        author = 'LiuLang',
        author_email = 'gsushzhsosgsu@gmail.com',

        packages = ['qr_gui', ],
        scripts = scripts,
        data_files = build_data_files(),
        )
