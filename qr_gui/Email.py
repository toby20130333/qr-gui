
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Widgets

class Email(Gtk.Box):
    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.app = app

        self.pack_start(Widgets.Label('Email Address:'), False, False, 0)
        self.email_entry = Gtk.Entry()
        self.email_entry.props.input_purpose = Gtk.InputPurpose.EMAIL
        self.pack_start(self.email_entry, False, False, 0)
        self.email_entry.connect('changed', self.on_changed)

        self.pack_start(Widgets.Label('Subject:'), False, False, 0)
        self.subject_entry = Gtk.Entry()
        self.pack_start(self.subject_entry, False, False, 0)
        self.subject_entry.connect('changed', self.on_changed)

        self.pack_start(Widgets.Label('Message:'), False, False, 0)
        message_win = Gtk.ScrolledWindow()
        self.pack_start(message_win, True, True, 0)

        self.message_buf = Gtk.TextBuffer()
        self.message_buf.connect('changed', self.on_changed)
        message_tv = Gtk.TextView(buffer=self.message_buf)
        message_tv.props.wrap_mode = Gtk.WrapMode.CHAR
        message_win.add(message_tv)

    def on_changed(self, *args):
        self.app.encode_txt = ''.join([
            'MATMSG:TO:', self.email_entry.get_text(),
            ';SUB:', self.subject_entry.get_text(),
            ';BODY:', Widgets.get_buf_text(self.message_buf),
            ';;',
            ])
        self.app.qr_encode()
