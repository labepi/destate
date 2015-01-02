# vim: set fileencoding=utf-8 :

# Copyright (C) 2008 Joao Paulo de Souza Medeiros.
#
# Author: João Paulo de Souza Medeiros <ignotus21@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import gtk


class Canvas(gtk.DrawingArea):
    """
    """
    def __init__(self):
        """
        """
        gtk.DrawingArea.__init__(self)

        self.__center_of_widget = (0, 0)

        self.__image = None

        self.__button1_press = None
        self.__button2_press = None
        self.__button3_press = None

        self.__scale = 1.0
        self.__translation = (0, 0)

        self.__last_motion_point = None

        self.__image = None

        self.connect('expose_event', self.expose)
        self.connect('button_press_event', self.button_press)
        self.connect('button_release_event', self.button_release)
        self.connect('motion_notify_event', self.motion_notify)
        self.connect('enter_notify_event', self.enter_notify)
        self.connect('leave_notify_event', self.leave_notify)
        self.connect('key_press_event', self.key_press)
        self.connect('key_release_event', self.key_release)
        self.connect('scroll_event', self.scroll_event)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.ENTER_NOTIFY |
                        gtk.gdk.LEAVE_NOTIFY |
                        gtk.gdk.MOTION_NOTIFY |
                        gtk.gdk.NOTHING |
                        gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.SCROLL_MASK)

        self.set_flags(gtk.CAN_FOCUS)
        self.grab_focus()


    def image_exists(function):
        """
        """
        def check_image_status(*args):

            if args[0].__image == None:
                return False

            return function(*args)

        return check_image_status


    def set_image(self, image):
        """
        """
        self.__image = image

        self.queue_draw()


    def get_image(self):
        """
        """
        return self.__image


    def set_scale(self, scale):
        """
        """
        if scale >= 0.01:

            self.__scale = scale
            self.queue_draw()


    def scroll_event(self, widget, event):
        """
        """
        if event.direction == gtk.gdk.SCROLL_UP:
            self.set_scale(self.__scale + 0.01)

        if event.direction == gtk.gdk.SCROLL_DOWN:
            self.set_scale(self.__scale - 0.01)

        self.queue_draw()


    def key_press(self, widget, event):
        """
        """
        key = gtk.gdk.keyval_name(event.keyval)

        if key == 'KP_Add':
            self.set_scale(self.__scale + 0.01)

        elif key == 'KP_Subtract':
            self.set_scale(self.__scale - 0.01)

        self.queue_draw()

        return True


    def key_release(self, widget, event):
        """
        """
        key = gtk.gdk.keyval_name(event.keyval)

        if key == 'c':
            self.__translation = (0, 0)

        if key == 's':
            self.__scale = 1.0

        self.queue_draw()

        return True


    def enter_notify(self, widget, event):
        """
        """
        self.grab_focus()

        return False


    def leave_notify(self, widget, event):
        """
        """
        return False


    def button_press(self, widget, event):
        """
        """
        if event.button == 1:
            self.__button1_press = True

        if event.button == 2:
            self.__button2_press = True

        if event.button == 3:
            self.__button3_press = True

        self.grab_focus()

        return False


    def button_release(self, widget, event):
        """
        """
        if event.button == 1:
            self.__button1_press = False

        if event.button == 2:
            self.__button2_press = False

        if event.button == 3:
            self.__button3_press = False

        self.grab_focus()

        return False


    def motion_notify(self, widget, event):
        """
        """
        pointer = self.get_pointer()

        if self.__button1_press == True and self.__last_motion_point != None:

            ax, ay = pointer
            ox, oy = self.__last_motion_point
            tx, ty = self.__translation

            self.__translation = (tx + ax - ox, ty - ay + oy)

        self.__last_motion_point = pointer

        self.grab_focus()
        self.queue_draw()
        
        return False


    def expose(self, widget, event):
        """
        """
        self.context = widget.window.cairo_create()

        self.context.rectangle(*event.area)
        self.context.set_source_rgb(1.0, 1.0, 1.0)
        self.context.fill()

        self.__draw()

        return False


    @image_exists
    def __draw(self):
        """
        """
        # getting allocation reference
        allocation = self.get_allocation()

        self.__center_of_widget = (allocation.width / 2,
                                   allocation.height / 2)

        aw, ah = allocation.width, allocation.height
        xc, yc = self.__center_of_widget

        ax, ay = self.__translation

        # xc = 320 yc = 240

        # -1.5 | -0.5 ( 480,  360)
        # -1.0 |  0.0 ( 320,  240)
        # -0.5 |  0.5 ( 160,  120)
        #  0.0 |  1.0 (   0,    0)
        #  0.5 |  1.5 (-160, -120)
        #  1.0 |  2.0 (-320, -240)
        #  1.5 |  2.5 (-480, -360)

        # scaling and translate
        factor = -(self.__scale - 1)

        self.context.translate(xc * factor + ax, yc * factor - ay)

        if self.__scale != 1.0:
            self.context.scale(self.__scale, self.__scale)

        # draw image
        if self.__image != None:

            x = self.__image.get_width()
            y = self.__image.get_height()

            self.context.set_source_pixbuf(self.__image,
                                           round(xc - x / 2),
                                           round(yc - y / 2))

            self.context.paint()
