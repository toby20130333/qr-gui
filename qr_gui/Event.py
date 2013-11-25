
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Widgets


class Event(Gtk.ScrolledWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(box)

        box.pack_start(Widgets.Label('Event Name:'), False, False, 0)

        self.name_entry = Gtk.Entry()
        self.name_entry.connect('changed', self.on_changed)
        box.pack_start(self.name_entry, False, False, 0)

        box.pack_start(Widgets.Label('Start Date & Time:'), False, False, 0)

        self.start_cal = Gtk.Calendar()
        self.start_cal.connect('day-selected', self.on_changed)
        self.start_cal.connect('month-changed', self.on_changed)
        self.start_cal.connect('next-year', self.on_changed)
        box.pack_start(self.start_cal, False, False, 0)

        start_box = Gtk.Box()
        box.pack_start(start_box, False, False, 0)

        self.start_hour = Gtk.SpinButton.new_with_range(0, 23, 1)
        self.start_hour.connect('value-changed', self.on_changed)
        start_box.pack_start(self.start_hour, False, False, 0)

        start_box.pack_start(Gtk.Label(':'), False, False, 0)

        self.start_min = Gtk.SpinButton.new_with_range(0, 59, 1)
        self.start_min.connect('value-changed', self.on_changed)
        start_box.pack_start(self.start_min, False, False, 0)

        box.pack_start(Widgets.Label('Stop Date & Time:'), False, False, 0)

        self.stop_cal = Gtk.Calendar()
        self.stop_cal.connect('day-selected', self.on_changed)
        self.stop_cal.connect('month-changed', self.on_changed)
        self.stop_cal.connect('next-year', self.on_changed)
        box.pack_start(self.stop_cal, False, False, 0)

        stop_box = Gtk.Box()
        box.pack_start(stop_box, False, False, 0)

        self.stop_hour = Gtk.SpinButton.new_with_range(0, 23, 1)
        self.stop_hour.connect('value-changed', self.on_changed)
        stop_box.pack_start(self.stop_hour, False, False, 0)

        stop_box.pack_start(Gtk.Label(':'), False, False, 0)

        self.stop_min = Gtk.SpinButton.new_with_range(0, 59, 1)
        self.stop_min.connect('value-changed', self.on_changed)
        stop_box.pack_start(self.stop_min, False, False, 0)

        box.pack_start(Widgets.Label('Event Location:'), False, False, 0)

        self.loc_entry = Gtk.Entry()
        self.loc_entry.connect('changed' ,self.on_changed)
        box.pack_start(self.loc_entry, False, False, 0)

    def on_changed(self, *args):
        start_time = Widgets.get_datetime(self.start_cal, self.start_hour,
                self.start_min)
        stop_time = Widgets.get_datetime(self.stop_cal, self.stop_hour,
                self.stop_min)
        self.app.encode_txt = ''.join([
            'BEGIN:VCALENDAR', '\n',
            'VERSION:2.0', '\n',
            'BEGIN:VEVENT', '\n',
            'SUMMARY;CHARSET=utf-8:', self.name_entry.get_text(), '\n',
            'LOCATION;CHARSET=utf-8:', self.loc_entry.get_text(), '\n',
            'DTSTART:', start_time, '\n',
            'DTEND:', stop_time, '\n',
            'END:VEVENT', '\n',
            'END:VCALENDAR',
            ])
        self.app.qr_encode()
