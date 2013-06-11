# Handler for GUI.

from gi.repository import Gdk
from gi.repository import Gtk
import math
import os
import shutil
import subprocess

from qrencodegui import Config


class Handler():
    def __init__(self, builder):
        self.builder = builder
        self.conf = Config.load_conf()

        self.MAX_TXT = 1024
        self.png_path = os.path.join('/dev/shm', 
                'qrencode-gui-' + str(os.getpid()) + '.png')

        self.window = builder.get_object('main_window')
        self.image = builder.get_object('image_qr')

        self.data_type = 0
        data_type = builder.get_object('comboboxtext_type')
        data_type.set_active(self.data_type)

        scrolled = builder.get_object('scrolledwindow_left')
        textview = builder.get_object('textview_text')
        textview.reparent(scrolled)

        self.on_pref_changed(init=True)

    def _get_text_from_buffer(self, buf):
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

    def _alert(self, txt):
        alert = Gtk.MessageDialog(
                self.window,
                Gtk.DialogFlags.MODAL,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                txt)
        alert.run()
        alert.destroy()

    def _len2(self, txt):
        if len(txt) == 1:
            return '0' + txt
        elif len(txt) == 0:
            return '00'
        return txt

    def _oct_to_hex(self, oct):
        num = str(hex(math.ceil(oct * 255)))[2:]
        return self._len2(num)

    def _color_to_str(self, color):
        rgba = Gdk.RGBA()
        rgba.parse(color)
        return ''.join([self._oct_to_hex(rgba.red),
                    self._oct_to_hex(rgba.green),
                    self._oct_to_hex(rgba.blue),
                    self._oct_to_hex(rgba.alpha)
                ])

    def _generate_image(self, txt):
        #print('_generate image()')
        #print('text is:')
        #print(txt)
        errors = ('L', 'M', 'Q', 'H')
        
        if len(txt) > self.MAX_TXT:
            self._alert('No more than 512 characters!')
            return False

        subprocess.Popen([
            'qrencode',
            '-o', self.png_path,
            '-s', str(int(self.conf['size'])),
            '-m', str(int(self.conf['margin'])),
            '-l', errors[self.conf['error']],
            '--foreground', self._color_to_str(self.conf['fg']),
            '--background', self._color_to_str(self.conf['bg']),
            txt,
        ]).wait()
        # Reload qr image in the window:
        self.image.set_from_file(self.png_path)

    def _update_statusbar(self, txt):
        statusbar = self.builder.get_object('statusbar_main')
        c1 = statusbar.get_context_id('count')
        status = 'Chracter count: {0}/{1}'.format(len(txt), 
                self.MAX_TXT)
        if len(txt) > self.MAX_TXT:
            status += ' No more than 512 characters!'
        statusbar.push(c1, status)

    def _get_txt_txt(self):
        buf = self.builder.get_object('textbuffer_text')
        return self._get_text_from_buffer(buf)

    def _get_email_txt(self):
        email_addr = self.builder.get_object('entry_email_address')
        email_sub = self.builder.get_object('entry_email_subject')
        email_msg_buf = self.builder.get_object('textbuffer_email_msg')
        return ''.join(['MATMSG:TO:', email_addr.get_text(),
                ';SUB:', email_sub.get_text(),
                ';BODY:', self._get_text_from_buffer(email_msg_buf),
                ';;',
                ])

    def _get_phone_txt(self):
        phone = self.builder.get_object('entry_phone_num')
        return 'tel:' + phone.get_text()

    def _get_addr_txt(self):
        names = ('entry_addr_first', 'entry_addr_last', 'entry_addr_org', 
                'entry_addr_job', 'entry_addr_phone', 'entry_addr_cell', 
                'entry_addr_fax', 'entry_addr_email', 
                'entry_addr_street', 'entry_addr_city', 'entry_addr_state',
                'entry_addr_zip', 'entry_addr_country',
                'entry_addr_website',
                )
        objs = [self.builder.get_object(name).get_text() for name in names]
        #print(objs)

        return ''.join(['BEGIN:VCARD', '\n', 
            'VERSION:3.0', '\n',
            'N:', objs[1], ';', objs[0], ';;;', '\n',
            'FN:', objs[0], ' ', objs[1], '\n',
            'ORG;:', objs[2], '\n',
            'TITLE:', objs[3], '\n',
            'TEL;TYPE=HOME:', objs[4], '\n',
            'TEL;TYPE=CELL:', objs[5], '\n',
            'TEL;TYPE=FAX:', objs[6], '\n',
            'EMAIL;TYPE=HOME:', objs[7], '\n',
            'ADR;TYPE=HOME:;;', objs[8], ';', objs[9], ';', objs[10],
            ';', objs[11], ';', objs[12], '\n',
            'URL:', objs[13], '\n',
            'END:VCARD',
            ])


    def _get_sms_txt(self):
        sms_phone = self.builder.get_object('entry_sms_phone')
        sms_msg = self.builder.get_object('textbuffer_sms_msg')
        sms_label = self.builder.get_object('label_sms_count')
        msg = self._get_text_from_buffer(sms_msg)
        sms_label.set_text('Message count: {0}/140'.format(len(msg)))
        return ''.join(['SMSTO:', sms_phone.get_text(), ':', msg,])

    def _get_geo_txt(self):
        geo_lat = self.builder.get_object('entry_geo_lat')
        geo_lon = self.builder.get_object('entry_geo_lon')
        return ''.join(['geo:' + geo_lat.get_text(), 
                ',', geo_lon.get_text()
                ])

    def _get_wifi_txt(self):
        wifi_types = ('nopass', 'WEP', 'WPA')
        wifi_type = self.builder.get_object('comboboxtext_wifi_type')
        wifi_ssid = self.builder.get_object('entry_wifi_ssid')
        wifi_pass = self.builder.get_object('entry_wifi_password')
        return ''.join(['WIFI:T:', wifi_types[wifi_type.get_active()],
                'S:', wifi_ssid.get_text(),
                'P:', wifi_pass.get_text(),
                ';;',
                ])

    def _get_cal_txt(self):
        names = ('entry_cal_name',
                'calendar_cal_start',
                'spinbutton_cal_start_hour', 
                'spinbutton_cal_start_minute',
                'calendar_cal_stop',
                'spinbutton_cal_stop_hour',
                'spinbutton_cal_stop_minute',
                'entry_cal_loc',
                )
        objs = [self.builder.get_object(name) for name in names]

        def get_date_time(calc, hour, minute):
            date = calc.get_date()
            hour = hour.get_text()
            minute = minute.get_text()
            return ''.join([self._len2(str(date[0])),
                        self._len2(str(date[1])),
                        self._len2(str(date[2])),
                    'T', self._len2(hour), self._len2(minute),
                    '00Z',
                    ])
        start_time = get_date_time(objs[1], objs[2], objs[3])
        stop_time = get_date_time(objs[4], objs[5], objs[6])

        return ''.join(['BEGIN:VCALENDAR', "\n",
                'VERSION:2.0', "\n",
                'BEGIN:VEVENT', "\n",
                'SUMMARY;CHARSET=utf-8:', objs[0].get_text(), "\n",
                'LOCATION;CHARSET=utf-8:', objs[7].get_text(), "\n",
                'DTSTART:', start_time, "\n",
                'DTEND:', stop_time, "\n",
                'END:VEVENT', "\n",
                'END:VCALENDAR', "\n"
                ])

    def generate(self, *args):
        #print('generate()')
        funcs = (self._get_txt_txt,
                self._get_email_txt,
                self._get_phone_txt,
                self._get_addr_txt,
                self._get_sms_txt,
                self._get_geo_txt,
                self._get_wifi_txt,
                self._get_cal_txt,
                )

        txt = funcs[self.data_type]()
        self._update_statusbar(txt)
        self._generate_image(txt)


    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, widget, event=None):
        # clearning...
        if os.path.exists(self.png_path):
            os.remove(self.png_path)
        Config.dump_conf(self.conf)
        Gtk.main_quit()

    # program configurations:
    def on_comboboxtext_type_changed(self, combo):
        old_data_type = self.data_type
        self.data_type = combo.get_active()
        scrolled = self.builder.get_object('scrolledwindow_left')
        type_lists = ['window_text', 'window_email', 'window_phone', 
                'window_addr', 'window_sms', 'window_geo', 'window_wifi', 
                'window_cal']
        win = self.builder.get_object(type_lists[self.data_type])
        old_win = self.builder.get_object(type_lists[old_data_type])
        child = win.get_children()[0]
        old_child = scrolled.get_children()[0]

        old_child.reparent(old_win)
        child.reparent(scrolled)


    def on_pref_changed(self, *args, init=False):
        size = self.builder.get_object('spinbutton_size')
        error = self.builder.get_object('comboboxtext_error')
        margin = self.builder.get_object('spinbutton_margin')
        fg = self.builder.get_object('colorbutton_fg')
        bg = self.builder.get_object('colorbutton_bg')

        if init == False:
            self.conf['size'] = size.get_value()
            self.conf['error'] = error.get_active()
            self.conf['margin'] = margin.get_value()
            self.conf['fg'] = fg.get_rgba().to_string()
            self.conf['bg'] = bg.get_rgba().to_string()
            self.generate()
        else:
            size.set_value(self.conf['size'])
            error.set_active(self.conf['error'])
            margin.set_value(self.conf['margin'])
            fg_color = Gdk.RGBA()
            fg_color.parse(self.conf['fg'])
            fg.set_rgba(fg_color)
            bg_color = Gdk.RGBA()
            bg_color.parse(self.conf['bg'])
            bg.set_rgba(bg_color)


    def on_button_save_clicked(self, btn):
        if not os.path.exists(self.png_path):
            return False

        dialog = Gtk.FileChooserDialog('Save image as..', 
                self.window,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter_png = Gtk.FileFilter()
        filter_png.set_name('PNG Image(*.png)')
        filter_png.add_mime_type('image/png')
        dialog.add_filter(filter_png)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(os.path.basename(self.png_path))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            targ_path = dialog.get_filename()
            shutil.copy(self.png_path, targ_path)
        dialog.destroy()

    def on_about_button_clicked(self, btn):
        aboutdialog = self.builder.get_object('aboutdialog')
        aboutdialog.run()
        aboutdialog.hide()
