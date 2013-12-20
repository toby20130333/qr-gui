
# Copyright (C) 2013-2014 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Config
_ = Config._
from qr_gui import Widgets

class Geo(Gtk.Box):
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.app = app

        self.pack_start(Widgets.Label(_('Latitude:')), False, False, 0)

        self.lat_entry = Gtk.Entry()
        self.pack_start(self.lat_entry, False, False, 0)
        self.lat_entry.connect('changed', self.on_changed)

        self.pack_start(Widgets.Label(_('Longtitude:')), False, False, 0)

        self.lont_entry = Gtk.Entry()
        self.pack_start(self.lont_entry, False, False, 0)
        self.lont_entry.connect('changed', self.on_changed)

    def on_changed(self, *args):
        self.app.encode_txt = ''.join([
            'geo:' + self.lat_entry.get_text(), 
            ',', self.lont_entry.get_text(),
            ])
        self.app.qr_encode()
