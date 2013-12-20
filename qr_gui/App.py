
# Copyright (C) 2013-2014 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gtk
import os
import shutil
import subprocess
GLib.threads_init()

from qr_gui import Config
_ = Config._
from qr_gui import Widgets
from qr_gui.Addr import Addr
from qr_gui.Email import Email
from qr_gui.Event import Event
from qr_gui.Geo import Geo
from qr_gui.Phone import Phone
from qr_gui.SelectArea import SelectArea
from qr_gui.SMS import SMS
from qr_gui.Text import Text
from qr_gui.WiFi import WiFi

QR_TYPES = (_('Plain Text'),
            _('Email Message'),
            _('Phone Number'),
            _('Addressbook'),
            _('SMS'),
            _('Geo Location'),
            _('WiFi Connection'),
            _('Event'))
ERROR_LEVELS = ('L', 'M', 'Q', 'H', )
ERROR_LEVELS_DISNAME = (_('Lowest'),
                        _('Medium'),
                        _('QuiteGood'),
                        _('Highest'))
MAX_LEN = 512 # 1024


class App():
    def __init__(self):
        self.conf = Config.load_conf()
        self._qr_encode_text = ''
        self.decode_path = ''
        self.encode_path = ''

        self.window = Gtk.Window()
        self.window.set_title(Config.APPNAME)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_icon_name('qr-gui')
        self.window.set_border_width(5)
        self.window.set_default_size(*self.conf['window-size'])
        self.window.connect('delete-event', self.on_app_exit)

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window.add(main_vbox)

        paned = Gtk.Paned()
        main_vbox.pack_start(paned, True, True, 0)
        self.statusbar = Gtk.Statusbar()
        main_vbox.pack_start(self.statusbar, False, False, 0)

        # left side of paned
        left_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        paned.add1(left_vbox)
        right_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        paned.add2(right_vbox)

        self.type_combo = Gtk.ComboBoxText()
        for item in QR_TYPES:
            self.type_combo.append_text(item)
        self.type_combo.set_active(0)
        self.type_combo.props.margin_bottom = 5
        self.type_combo.connect('changed', self.on_type_combo_changed)
        left_vbox.pack_start(self.type_combo, False, False, 0)

        self.type_nb = Gtk.Notebook()
        self.type_nb.set_show_tabs(False)
        #self.type_nb.props.width_request = 300
        left_vbox.pack_start(self.type_nb, True, True, 0)
        self.init_type_nb()

        # right side of paned
        opt_grid = Gtk.Grid()
        opt_grid.set_column_spacing(15)
        opt_grid.attach(Widgets.Label(_('Pixel Size:')), 0, 0, 1, 1)
        opt_grid.attach(Widgets.Label(_('Error Correction:')), 1, 0, 1, 1)
        opt_grid.attach(Widgets.Label(_('Margin Size:')), 2, 0, 1, 1)
        opt_grid.attach(Widgets.Label(_('Foreground:')), 3, 0, 1, 1)
        opt_grid.attach(Widgets.Label(_('Background:')), 4, 0, 1, 1)

        pixel_spin = Gtk.SpinButton.new_with_range(1, 15, 1)
        pixel_spin.set_value(self.conf['pixel'])
        pixel_spin.connect('value-changed', self.on_pixel_spin_changed)
        opt_grid.attach(pixel_spin, 0, 1, 1, 1)

        error_level_comb = Gtk.ComboBoxText()
        for item in ERROR_LEVELS_DISNAME:
            error_level_comb.append_text(item)
        error_level_comb.set_active(0)
        error_level_comb.connect('changed', self.on_error_level_changed)
        opt_grid.attach(error_level_comb, 1, 1, 1, 1)

        margin_spin = Gtk.SpinButton.new_with_range(1, 25, 1)
        margin_spin.set_value(self.conf['margin'])
        margin_spin.connect('value-changed', self.on_margin_spin_changed)
        opt_grid.attach(margin_spin, 2, 1, 1, 1)

        fore_color = Gtk.ColorButton()
        fore_color.set_use_alpha(True)
        color = Gdk.RGBA()
        color.parse(self.conf['fg'])
        fore_color.set_rgba(color)
        fore_color.connect('color-set', self.on_fore_color_set)
        opt_grid.attach(fore_color, 3, 1, 1, 1)

        back_color = Gtk.ColorButton()
        back_color.set_use_alpha(True)
        color.parse(self.conf['bg'])
        back_color.set_rgba(color)
        back_color.connect('color-set', self.on_back_color_set)
        opt_grid.attach(back_color, 4, 1, 1, 1)
        right_vbox.pack_start(opt_grid, False, False, 0)
        opt_grid.props.halign = Gtk.Align.END

        img_win = Gtk.ScrolledWindow()
        right_vbox.pack_start(img_win, True, True, 0)

        viewport = Gtk.Viewport()
        img_win.add(viewport)

        self.image = Gtk.Image()
        self.image.set_from_file(Config.APP_LOGO)
        viewport.add(self.image)

        control_bar = Gtk.Toolbar()
        control_bar.set_icon_size(5)
        #control_bar.set_style(Gtk.ToolbarStyle.BOTH)
        control_bar.get_style_context().add_class(Gtk.STYLE_CLASS_MENUBAR)
        control_bar.props.show_arrow = False
        right_vbox.pack_start(control_bar, False, False, 0)

        save_item = Gtk.ToolButton(label=_('Save'))
        save_item.set_tooltip_text(_('Save QR Image to file'))
        save_item.set_icon_name('document-save-symbolic')
        save_item.connect('clicked', self.on_save_btn_clicked)
        control_bar.insert(save_item, 0)

        open_item = Gtk.ToolButton(label=_('Scan QR Image'))
        open_item.set_tooltip_text(_('Scan QR from QR Image'))
        open_item.set_icon_name('document-open-symbolic')
        open_item.props.halign = Gtk.Align.END
        open_item.connect('clicked', self.on_open_btn_clicked)
        control_bar.insert(open_item, 1)
        control_bar.child_set_property(open_item, 'expand', True)

        cam_item = Gtk.ToolButton(label=_('Scan from WebCam'))
        cam_item.set_tooltip_text(_('Scan QR from WebCam'))
        cam_item.set_icon_name('camera-web-symbolic')
        cam_item.connect('clicked', self.on_cam_btn_clicked)
        control_bar.insert(cam_item, 2)

        grab_item = Gtk.ToolButton(label=_('Grab QR from Screen'))
        grab_item.set_tooltip_text(_('Scan QR from Screen'))
        grab_item.set_icon_name('applets-screenshooter-symbolic')
        grab_item.connect('clicked', self.on_grab_btn_clicked)
        control_bar.insert(grab_item, 3)

    def init_type_nb(self):
        tabs = [
                Text(self),
                Email(self),
                Phone(self),
                Addr(self),
                SMS(self),
                Geo(self),
                WiFi(self),
                Event(self),
                ]
        self.text_tab = tabs[0]
        for i, tab in enumerate(tabs):
            self.type_nb.append_page(tab, Gtk.Label(QR_TYPES[i]))

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, *args):
        if os.path.exists(self.encode_path):
            os.remove(self.encode_path)
        if os.path.exists(self.decode_path):
            os.remove(self.decode_path)
        Config.dump_conf(self.conf)
        Gtk.main_quit()

    def reset(self):
        '''Reset QR generation process'''
        self.qr_encode('')

    def refresh(self):
        self.qr_encode(self._qr_encode_text)

    def qr_encode(self, text):
        '''Encode txt to QR image and displays on main window.'''
        length = len(text)
        self._qr_encode_text = text
        self.update_statusbar(length)
        if length == 0:
            self.image.set_from_file(Config.APP_LOGO)
            return False
        elif length > MAX_LEN:
            return False

        if os.path.exists(self.encode_path):
            os.remove(self.encode_path)
        self.encode_path = Widgets.generate_path()

        # TODO: check `qrencode` command exists
        subprocess.Popen([
            'qrencode',
            '-o', self.encode_path,
            '-s', str(int(self.conf['pixel'])),
            '-m', str(int(self.conf['margin'])),
            '-l', ERROR_LEVELS[self.conf['error']],
            '--foreground', Widgets.color_to_str(self.conf['fg']),
            '--background', Widgets.color_to_str(self.conf['bg']),
            text,
        ]).wait()

        # Reload qr image in the window:
        self.image.set_from_file(self.encode_path)

    def qr_decode(self):
        if not os.path.exists(self.decode_path):
            return
        p = subprocess.Popen([
            'zbarimg',
            '--raw',
            '--quiet',
            self.decode_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out_txt = out.decode()

        if len(out_txt) == 0:
            Widgets.error(_('Failed to decode QR Image'), self.window)
            return

        dialog = Gtk.Dialog(_('QR Image Content'), self.window, 0,
                (Gtk.STOCK_COPY, Gtk.ResponseType.YES,
                 Gtk.STOCK_EDIT, Gtk.ResponseType.APPLY,
                 Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE))

        box = dialog.get_content_area()
        content_win = Gtk.ScrolledWindow()
        content_win.set_size_request(480, 320)
        box.add(content_win)

        buf = Gtk.TextBuffer()
        buf.set_text(out_txt)
        tv = Gtk.TextView(buffer=buf)
        tv.props.wrap_mode = Gtk.WrapMode.CHAR
        content_win.add(tv)

        box.show_all()
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.CLOSE:
            return
        elif response == Gtk.ResponseType.YES:
            clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clip.set_text(out_txt, -1)
            clip.store()
        elif response == Gtk.ResponseType.APPLY:
            self.type_combo.set_active(0)
            self.text_tab.set_text(out_txt)

    def update_statusbar(self, length):
        '''Update image path and character count on statusbar'''
        count_id = self.statusbar.get_context_id('count')
        status = _('Characters: {0}/{1}').format(length, MAX_LEN)
        if length > MAX_LEN:
            status += _(' Error: No more than {0} characters!').format(MAX_LEN)
        self.statusbar.push(count_id, status)

    # opt_grid signal handlers
    def on_type_combo_changed(self, combo):
        self.type_nb.set_current_page(combo.get_active())

    def on_pixel_spin_changed(self, spin):
        self.conf['pixel'] = spin.get_value()
        self.refresh()

    def on_error_level_changed(self, combo):
        self.conf['error'] = combo.get_active()
        self.refresh()

    def on_margin_spin_changed(self, spin):
        self.conf['margin'] = spin.get_value()
        self.refresh()

    def on_fore_color_set(self, color_btn):
        self.conf['fg'] = color_btn.get_rgba().to_string()
        self.refresh()

    def on_back_color_set(self, color_btn):
        self.conf['bg'] = color_btn.get_rgba().to_string()
        self.refresh()

    # controlbar signal handlers
    def on_save_btn_clicked(self, btn):
        if not os.path.exists(self.encode_path):
            return

        dialog = Gtk.FileChooserDialog(_('Save QR image as..'),
                self.window, Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        png_filter = Gtk.FileFilter()
        png_filter.set_name(_('PNG Image'))
        png_filter.add_mime_type('image/png')
        dialog.add_filter(png_filter)
        all_filter = Gtk.FileFilter()
        all_filter.set_name(_('All Files'))
        all_filter.add_pattern('*.*')
        dialog.add_filter(all_filter)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(os.path.basename(self.encode_path))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            targ_path = dialog.get_filename()
            shutil.copy(self.encode_path, targ_path)
        dialog.destroy()

    def on_open_btn_clicked(self, btn):
        dialog = Gtk.FileChooserDialog(_('Choose a QR image to Scan..'),
                self.window, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        img_filter = Gtk.FileFilter()
        img_filter.set_name(_('Image Files'))
        img_filter.add_mime_type('image/png')
        img_filter.add_mime_type('image/svg')
        img_filter.add_mime_type('image/jpg')
        img_filter.add_mime_type('image/tiff')
        img_filter.add_mime_type('image/gif')
        dialog.add_filter(img_filter)
        all_filter = Gtk.FileFilter()
        all_filter.set_name(_('All Files'))
        all_filter.add_pattern('*.*')
        dialog.add_filter(all_filter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if os.path.exists(self.decode_path):
                os.remove(self.decode_path)
            self.decode_path = Widgets.generate_path()
            targ_path = dialog.get_filename()
            shutil.copy(targ_path, self.decode_path)
            GLib.timeout_add(100, self.qr_decode)
        dialog.destroy()

    def on_cam_btn_clicked(self, btn):
        pass

    def on_grab_btn_clicked(self, btn):
        def _do_screenshot(rect_list):
            pix = Widgets.take_select_screenshot(*rect_list)
            if pix is None:
                self.window.present()
                return
            if os.path.exists(self.decode_path):
                os.remove(self.decode_path)
            self.decode_path = Widgets.generate_path()
            status = Widgets.save_pix_to_file(pix, self.decode_path)
            if status is True:
                GLib.timeout_add(100, self.qr_decode)
            self.window.present()

        def _on_selected(select_area, rect):
            rect_list =(rect.x, rect.y, rect.width, rect.height)
            GLib.timeout_add(200, _do_screenshot, rect_list)

        def _on_no_selected(*args):
            self.window.present()

        self.window.hide()
        select_area = SelectArea()
        select_area.connect('selected', _on_selected)
        select_area.connect('no-select', _on_no_selected)
        select_area.run()
