
# Copyright (C) 2013-2014 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import cairo
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
import time


class SelectArea(Gtk.Window):
    __gsignals__ = {
            'selected': (
                GObject.SIGNAL_RUN_LAST, 
                None, (Gdk.Rectangle, )),
            'no-select': (
                GObject.SIGNAL_RUN_LAST,
                None, (Gdk.Rectangle, )),
            }
    def __init__(self):
        super().__init__()
        self.set_decorated(False)
        screen = Gdk.Screen.get_default()
        visual = screen.get_rgba_visual()

        self.rect = Gdk.Rectangle()
        self.button_pressed = False
        self.aborted = False

        if screen.is_composited() and visual:
            self.set_visual(visual)
            self.set_app_paintable(True)

        self.connect('key-press-event', self.on_window_key_press)
        self.connect('button-press-event',
                self.on_window_button_press)
        self.connect('button-release-event',
                self.on_window_button_release)
        self.connect('motion-notify-event',
                self.on_window_motion_notify)
        self.move(-100, -100)
        self.resize(10, 10)

    def run(self):
        self.show()

        cursor = Gdk.Cursor.new(Gdk.CursorType.CROSSHAIR)
        display = Gdk.Display.get_default()
        manager = display.get_device_manager()
        pointer = manager.get_client_pointer()
        keyboard = pointer.get_associated_device()
        gdk_window = self.get_window()

        res = pointer.grab(gdk_window,
                Gdk.GrabOwnership.NONE, False, 
                Gdk.EventMask.POINTER_MOTION_MASK |
                Gdk.EventMask.BUTTON_PRESS_MASK |
                Gdk.EventMask.BUTTON_RELEASE_MASK |
                Gdk.EventMask.ALL_EVENTS_MASK,
                cursor, Gdk.CURRENT_TIME)
        while res != Gdk.GrabStatus.SUCCESS:
            time.sleep(0.1)
            res = pointer.grab(gdk_window,
                    Gdk.GrabOwnership.NONE, False, 
                    Gdk.EventMask.POINTER_MOTION_MASK |
                    Gdk.EventMask.BUTTON_PRESS_MASK |
                    Gdk.EventMask.BUTTON_RELEASE_MASK,
                    cursor, Gdk.CURRENT_TIME)

        res = keyboard.grab(gdk_window,
                Gdk.GrabOwnership.NONE, False, 
                Gdk.EventMask.KEY_PRESS_MASK |
                Gdk.EventMask.KEY_RELEASE_MASK,
                None, Gdk.CURRENT_TIME)
        while res != Gdk.GrabStatus.SUCCESS:
            time.sleep(0.1)
            res = keyboard.grab(gdk_window,
                    Gdk.GrabOwnership.NONE, False, 
                    Gdk.EventMask.KEY_PRESS_MASK |
                    Gdk.EventMask.KEY_RELEASE_MASK,
                    None, Gdk.CURRENT_TIME)

        Gtk.main()
        pointer.ungrab(Gdk.CURRENT_TIME)
        keyboard.ungrab(Gdk.CURRENT_TIME)
        Gdk.flush()
        self.outer()

    def outer(self, *args):
        if not self.aborted and self.rect.width > 0 and \
                self.rect.height > 0:
            self.emit('selected', self.rect)
        else:
            self.emit('no-select', self.rect)
        self.destroy()
        #Gtk.main_quit()

    def do_draw(self, cr):
        context = self.get_style_context()
        if self.get_app_paintable():
            cr.set_operator(cairo.OPERATOR_SOURCE)
            cr.set_source_rgba(0, 0, 0, 0)
            cr.paint()
            
            context.save()
            context.add_class(Gtk.STYLE_CLASS_RUBBERBAND)
            Gtk.render_background(context, cr, 0, 0,
                    self.get_allocated_width(),
                    self.get_allocated_height())
            Gtk.render_frame(context, cr, 0, 0,
                    self.get_allocated_width(),
                    self.get_allocated_height())
            context.restore()
        return True

    def on_window_key_press(self, window, event):
        if event.keyval == Gdk.KEY_Escape:
            self.rect.x = 0
            self.rect.y = 0
            self.rect.width = 0
            self.rect.height = 0
            self.aborted = True

            Gtk.main_quit()
        return True

    def on_window_button_press(self, window, event):
        if self.button_pressed:
            return True
        self.button_pressed = True
        self.rect.x = event.x_root
        self.rect.y = event.y_root
        return True

    def on_window_button_release(self, window, event):
        if not self.button_pressed:
            return True
        self.rect.width = abs(self.rect.x - event.x_root)
        self.rect.height = abs(self.rect.y - event.y_root)
        self.rect.x = min(self.rect.x, event.x_root)
        self.rect.y = min(self.rect.y, event.y_root)

        if self.rect.x == 0 or self.rect.y == 0:
            return True
        Gtk.main_quit()
        return True

    def on_window_motion_notify(self, window, event):
        print(self.get_app_paintable())
        if not self.button_pressed:
            return True
        draw_rect = Gdk.Rectangle()
        draw_rect.width = abs(self.rect.x - event.x_root)
        draw_rect.height = abs(self.rect.y - event.y_root)
        draw_rect.x = min(self.rect.x, event.x_root)
        draw_rect.y = min(self.rect.y, event.y_root)

        if draw_rect.x <= 0 or draw_rect.y <= 0:
            self.move(-100, -100)
            self.resize(10, 10)
            return True
        self.move(draw_rect.x, draw_rect.y)
        self.resize(draw_rect.width, draw_rect.height)
        return True
GObject.type_register(SelectArea)
