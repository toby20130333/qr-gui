
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Widgets


class SMS(Gtk.Box):
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.app = app

        self.pack_start(Widgets.Label('Phone Number:'), False, False, 0)

        self.phone_entry = Gtk.Entry()
        self.phone_entry.props.input_purpose = Gtk.InputPurpose.PHONE
        self.phone_entry.connect('changed', self.on_changed)
        self.pack_start(self.phone_entry, False, False, 0)

        self.pack_start(Widgets.Label('Message:'), False, False, 0)

        message_win = Gtk.ScrolledWindow()
        self.pack_start(message_win, True, True, 0)

        self.message_buf = Gtk.TextBuffer()
        self.message_buf.connect('changed', self.on_changed)
        message_tv = Gtk.TextView(buffer=self.message_buf)
        message_win.add(message_tv)

        self.count_label = Widgets.Label('Message chars: 0/140')
        self.count_label.props.margin_bottom = 5
        self.pack_start(self.count_label, False, False, 0)

    def on_changed(self, *args):
        msg = Widgets.get_buf_text(self.message_buf)
        self.count_label.set_text('Message chars: {0}/140'.format(len(msg)))
        self.app.encode_txt = ''.join([
            'SMSTO:', self.phone_entry.get_text(),
            ':', msg,
            ])
        self.app.qr_encode()
