# Handler for GUI.

from gettext import gettext as _
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os
import re
import shutil
import tempfile

from qrencodegui.Config import *

class Handler():
    def __init__(self, builder):
        self.builder = builder
        self.MAX_TXT = 512
        self.png_path = ''
        self._image_level = 7
        self.gene_btn = self.builder.get_object('generate_toolbutton')
        self.window = self.builder.get_object('main_window')

        self.image = builder.get_object('image')
        self.textview = builder.get_object('textview')

    def _alert(self, txt):
        alert = Gtk.MessageDialog(
                self.window,
                Gtk.DialogFlags.MODAL,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                txt)
        alert.run()
        alert.destroy()

    def _set_sensitive(self, widget_id, status=True):
        widget = self.builder.get_object(widget_id)
        widget.set_sensitive(status)

    def _resize_window(self):
        pixbuf = self.image.get_pixbuf()
        width = pixbuf.get_width() + 100
        height = pixbuf.get_height() + 20
        self.window.resize(width, height)

    def _quit(self):
        if os.path.exists(self.png_path):
            os.remove(self.png_path)
        Gtk.main_quit()

    def on_window_destroy(self, win):
        self._quit()

    def on_textbuffer_changed(self, buf):
        txt = self._get_text_from_buffer()
        if len(txt) == 0 or len(txt) > self.MAX_TXT:
            self.gene_btn.set_sensitive(False)
        else:
            self.gene_btn.set_sensitive(True)

    def _get_text_from_buffer(self):
        buf = self.builder.get_object('textbuffer')
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

    def on_generate_button_clicked(self, btn):
        self._generate_image()

        # Set buttons clickable:
        self._set_sensitive('zoom_in_toolbutton')
        self._set_sensitive('zoom_out_toolbutton')
        self._set_sensitive('save_toolbutton')

    def _generate_image(self):
        txt = self._get_text_from_buffer()
        txt = txt.replace('"', '\\"')
        
        if len(txt) > self.MAX_TXT:
            self._alert(_('No more than 512 characters!'))
            return False

        # Use qrencode command to generate png file:
        self.png_path = os.path.join(tempfile.gettempdir(), 
                _('qrencode-gui-') + str(os.getpid()) + '.png')
        cmd = ('qrencode -s ' + str(self._image_level) + ' -o ' + 
                self.png_path + ' "' + txt + '"')
        os.system(cmd)

        # Reload qr image in the window:
        self.image.set_from_file(self.png_path)
        self._resize_window()

    def on_zoom_in_button_clicked(self, btn):
        if self._image_level < 11:
            self._image_level += 1
            self._generate_image()

    def on_zoom_out_button_clicked(self, btn):
        if self._image_level > 4:
            self._image_level -= 1
            self._generate_image()

    def on_save_button_clicked(self, btn):
        if not os.path.exists(self.png_path):
            return False

        dialog = Gtk.FileChooserDialog(_('Save image as..'), 
                self.window,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter_png = Gtk.FileFilter()
        filter_png.set_name(_('PNG Image(*.png)'))
        filter_png.add_mime_type('image/png')
        dialog.add_filter(filter_png)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(os.path.basename(self.png_path))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            targ_path = dialog.get_filename()
            #print(targ_path)
            shutil.copy(self.png_path, targ_path)
        dialog.destroy()

    def on_about_button_clicked(self, btn):
        aboutdialog = self.builder.get_object('aboutdialog')
        aboutdialog.run()
        aboutdialog.hide()

    def on_quit_button_clicked(self, btn):
        self._quit()
