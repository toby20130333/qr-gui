# Handler for GUI.

from gi.repository import Gtk
from gi.repository import GLib
import os
import re
import shutil
import tempfile
import time


class Handler():
    def __init__(self, builder):
        self.builder = builder
        self.MAX_TXT = 512
        self._image_level = 7
        # use self.instant_time as global timestamp.
        self.instant_time = 0
        # do instant generation after 600ms.
        self.INSTANT_TIMEOUT = 600
        self.png_path = os.path.join(tempfile.gettempdir(), 
                'qrencode-gui-' + str(os.getpid()) + '.png')

        self.window = self.builder.get_object('main_window')
        self.gene_btn = self.builder.get_object('generate_toolbutton')

        self.image = builder.get_object('image')
        self.textview = builder.get_object('textview')
        self.textbuffer = builder.get_object('textbuffer')

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

    def _get_text_from_buffer(self):
        return self.textbuffer.get_text(self.textbuffer.get_start_iter(),
                self.textbuffer.get_end_iter(), False)

    def _generate_image(self):
        txt = self._get_text_from_buffer()
        txt = txt.replace('"', '\\"')
        
        if len(txt) > self.MAX_TXT:
            self._alert('No more than 512 characters!')
            return False

        # Use qrencode command to generate png file:
        cmd = ('qrencode -s ' + str(self._image_level) + ' -o ' + 
                self.png_path + ' "' + txt + '"')
        os.system(cmd)

        # Reload qr image in the window:
        self.image.set_from_file(self.png_path)
        self._resize_window()

        # Set buttons clickable:
        self._set_sensitive('zoom_in_toolbutton')
        self._set_sensitive('zoom_out_toolbutton')
        self._set_sensitive('save_toolbutton')

    def _instant_generate(self, localtime):
        # do instant generation only if local timestamp == global timestamp.
        if localtime == self.instant_time:
            self._generate_image()

    def on_window_destroy(self, win):
        self._quit()

    def on_textbuffer_changed(self, buf):
        txt = self._get_text_from_buffer()
        if len(txt) == 0 or len(txt) > self.MAX_TXT:
            self.gene_btn.set_sensitive(False)
        else:
            self.gene_btn.set_sensitive(True)
            self.instant_time = time.time()
            GLib.timeout_add(self.INSTANT_TIMEOUT,
                    self._instant_generate, self.instant_time)

    def on_generate_button_clicked(self, btn):
        self._generate_image()

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

    def on_quit_button_clicked(self, btn):
        self._quit()
