
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gdk
from gi.repository import Gtk
import math
import time

def generate_path():
    return '/dev/shm/qr-gui-{0}.png'.format(int(time.time()))

def get_buf_text(buf):
    return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

def error(msg, parent):
    dialog = Gtk.MessageDialog(
            parent,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK,
            msg)
    dialog.run()
    dialog.destroy()

def len2(txt):
    '''
    Return a string with two characters, prefixing with 0
    '''
    if len(txt) == 0:
        return '00'
    elif len(txt) == 1:
        return '0' + txt
    return txt[:2]

def oct2hex(oct_):
    return len2(str(hex(math.ceil(oct_ * 255)))[2:])

def color_to_str(color):
    rgba = Gdk.RGBA()
    rgba.parse(color)
    return ''.join([
        oct2hex(rgba.red),
        oct2hex(rgba.green),
        oct2hex(rgba.blue),
        oct2hex(rgba.alpha),
        ])

def get_datetime(calc, hour, minute):
    date = calc.get_date()
    hour = hour.get_text()
    minute = minute.get_text()
    return ''.join([
        len2(str(date[0])),
        len2(str(date[1])),
        len2(str(date[2])),
        'T',
        len2(hour),
        len2(minute),
        '00Z',
        ])

def take_select_screenshot(x_orig, y_orig, width, height):
    root_window = Gdk.get_default_root_window()
    pix = Gdk.pixbuf_get_from_window(root_window, x_orig, y_orig,
            width, height)
    return pix

def save_pix_to_file(pixbuf, filename, type_='png'):
    status, buf = pixbuf.save_to_bufferv(type_, [], [])
    if status is not True:
        return status
    with open(filename, 'wb') as fh:
        fh.write(buf)
    return True


class Label(Gtk.Label):
    '''
    A GtkLabel subclass which aligns left
    '''
    def __init__(self, *args):
        super().__init__(*args)
        self.props.xalign = 0
        self.props.margin_top = 5
