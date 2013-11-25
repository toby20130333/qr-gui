
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gtk

from qr_gui import Widgets


class Addr(Gtk.ScrolledWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(box)

        box.pack_start(Widgets.Label('First Name:'), False, False, 0) 

        self.first_name_entry = Gtk.Entry()
        self.first_name_entry.connect('changed', self.on_changed)
        box.pack_start(self.first_name_entry, False, False, 0)

        box.pack_start(Widgets.Label('Last Name:'), False, False, 0)

        self.last_name_entry = Gtk.Entry()
        self.last_name_entry.connect('changed', self.on_changed)
        box.pack_start(self.last_name_entry, False, False, 0)

        box.pack_start(Widgets.Label('Job Title:'), False, False, 0)

        self.job_entry = Gtk.Entry()
        self.job_entry.connect('changed', self.on_changed)
        box.pack_start(self.job_entry, False, False, 0)

        box.pack_start(Widgets.Label('Telephone Number:'), False, False, 0)

        self.phone_entry = Gtk.Entry()
        self.phone_entry.connect('changed', self.on_changed)
        box.pack_start(self.phone_entry, False, False, 0)

        box.pack_start(Widgets.Label('Cell Phone:'), False, False, 0)

        self.cell_entry = Gtk.Entry()
        self.cell_entry.connect('changed', self.on_changed)
        box.pack_start(self.cell_entry, False, False, 0)

        box.pack_start(Widgets.Label('Fax Nubmer:'), False, False, 0)

        self.fax_entry = Gtk.Entry()
        self.fax_entry.connect('changed', self.on_changed)
        box.pack_start(self.fax_entry, False, False, 0)

        box.pack_start(Widgets.Label('Email:'), False, False, 0)

        self.email_entry = Gtk.Entry()
        self.email_entry.connect('changed', self.on_changed)
        box.pack_start(self.email_entry, False, False, 0)

        box.pack_start(Widgets.Label('Website:'), False, False, 0)
        
        self.site_entry = Gtk.Entry()
        self.site_entry.connect('changed', self.on_changed)
        box.pack_start(self.site_entry, False, False, 0)

        box.pack_start(Widgets.Label('Organization:'), False, False, 0)

        self.org_entry = Gtk.Entry()
        self.org_entry.connect('changed', self.on_changed)
        box.pack_start(self.org_entry, False, False, 0)

        box.pack_start(Widgets.Label('Street Address:'), False, False, 0)

        self.street_entry = Gtk.Entry()
        self.street_entry.connect('changed', self.on_changed)
        box.pack_start(self.street_entry, False, False, 0)

        box.pack_start(Widgets.Label('City:'), False, False, 0)

        self.city_entry = Gtk.Entry()
        self.city_entry.connect('changed', self.on_changed)
        box.pack_start(self.city_entry, False, False, 0)

        box.pack_start(Widgets.Label('State:'), False, False, 0)

        self.state_entry = Gtk.Entry()
        self.state_entry.connect('changed', self.on_changed)
        box.pack_start(self.state_entry, False, False, 0)

        box.pack_start(Widgets.Label('Zip/Postcode:'), False, False, 0)

        self.zip_entry = Gtk.Entry()
        self.zip_entry.connect('changed', self.on_changed)
        box.pack_start(self.zip_entry, False, False, 0)

        box.pack_start(Widgets.Label('Country:'), False, False, 0)

        self.country_entry = Gtk.Entry()
        self.country_entry.connect('changed', self.on_changed)
        box.pack_start(self.country_entry, False, False, 0)

    def on_changed(self, *args):
        addr = [
            'BEGIN:VCARD', '\n',
            'VERSION:3.0', '\n',
            'N:',
                self.last_name_entry.get_text(), ';',
                self.first_name_entry.get_text(), ';;;',
                '\n',
            'FN:',
                self.first_name_entry.get_text(), ' ',
                self.last_name_entry.get_text(),
                '\n',
            'ADR;TYPE=HOME:;;',
                self.street_entry.get_text(), ';',
                self.city_entry.get_text(), ';',
                self.state_entry.get_text(), ';',
                self.zip_entry.get_text(), ';',
                self.country_entry.get_text(),
                '\n',
            ]
        if len(self.phone_entry.get_text()) > 0:
            addr.append('TEL;TYPE=HOME:')
            addr.append(self.phone_entry.get_text()),
            addr.append('\n')
        if len(self.cell_entry.get_text()) > 0:
            addr.append('TEL;TYPE=CELL:')
            addr.append(self.cell_entry.get_text())
            addr.append('\n')
        if len(self.fax_entry.get_text()) > 0:
            addr.append('TEL;TYPE=FAX')
            addr.append(self.fax_entry.get_text())
            addr.append('\n')
        if len(self.email_entry.get_text()) > 0:
            addr.append('EMAIL;TYPE=HOME:')
            addr.append(self.email_entry.get_text())
            addr.append('\n')
        if len(self.org_entry.get_text()) > 0:
            addr.append('ORG:')
            addr.append(self.org_entry.get_text())
            addr.append('\n')
        if len(self.job_entry.get_text()) > 0:
            addr.append('TITLE:')
            addr.append(self.job_entry.get_text())
            addr.append('\n')
        if len(self.site_entry.get_text()) > 0:
            addr.append('URL:')
            addr.append(self.site_entry.get_text())
            addr.append('\n')
        addr.append('END:VCARD')
        self.app.encode_txt = ''.join(addr)
        self.app.qr_encode()
