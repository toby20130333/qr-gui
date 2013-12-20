
# Copyright (C) 2013-2014 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Config
_ = Config._
from qr_gui import Widgets

WIFI_TYPES = ('nopass', 'WEP', 'WPA', )
WIFI_TYPES_DISNAME = (_('No Encryption'), _('WEP'), _('WPA/WPA2'), )

class WiFi(Gtk.Box):
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.app = app

        self.pack_start(Widgets.Label(_('Network Type:')), False, False, 0)

        self.type_combo = Gtk.ComboBoxText()
        for item in WIFI_TYPES_DISNAME:
            self.type_combo.append_text(item)
        self.type_combo.set_active(2)
        self.pack_start(self.type_combo, False, False, 0)
        self.type_combo.connect('changed', self.on_changed)

        self.pack_start(Widgets.Label(_('SSID:')), False, False, 0)

        self.ssid_entry = Gtk.Entry()
        self.pack_start(self.ssid_entry, False, False, 0)
        self.ssid_entry.connect('changed', self.on_changed)

        self.pack_start(Widgets.Label(_('Password:')), False, False, 0)

        self.password_entry = Gtk.Entry()
        self.pack_start(self.password_entry, False, False, 0)
        self.password_entry.connect('changed', self.on_changed)

        note_info = Gtk.InfoBar()
        note_info.props.margin_top = 20
        self.pack_start(note_info, False, False, 0)
        note_label = Gtk.Label(_('Works on Android!'))
        note_label.props.xalign = 1
        note_label.props.margin_top = 10
        note_label.props.margin_bottom = 5
        note_info.pack_start(note_label, False, False, 5)

    def on_changed(self, *args):
        self.app.encode_txt = ''.join([
            'WIFI:T:', WIFI_TYPES[self.type_combo.get_active()],
            'S:', self.ssid_entry.get_text(),
            'P:', self.password_entry.get_text(),
            ';;',
            ])
        self.app.qr_encode()
