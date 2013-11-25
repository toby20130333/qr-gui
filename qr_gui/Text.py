
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Widgets

class Text(Gtk.ScrolledWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.buf = Gtk.TextBuffer()
        self.buf.connect('changed', self.on_buf_changed)
        tv = Gtk.TextView(buffer=self.buf)
        self.add(tv)
        tv.props.wrap_mode = Gtk.WrapMode.CHAR

    def set_text(self, text):
        self.buf.set_text(text)

    def on_buf_changed(self, buf):
        self.app.encode_txt = Widgets.get_buf_text(buf)
        self.app.qr_encode()
