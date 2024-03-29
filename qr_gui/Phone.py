
# Copyright (C) 2013-2014 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Config
_ = Config._
from qr_gui import Widgets

class Phone(Gtk.Box):
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.app = app

        self.pack_start(Widgets.Label(_('Phone Number:')), False, False, 0)

        phone_entry = Gtk.Entry()
        phone_entry.props.input_purpose = Gtk.InputPurpose.PHONE
        phone_entry.connect('changed', self.on_phone_entry_changed)
        self.pack_start(phone_entry, False, False, 0)

    def on_phone_entry_changed(self, entry):
        if len(entry.get_text()) == 0:
            self.app.reset()
            return False

        text = 'tel:' + entry.get_text()
        self.app.qr_encode(text)
