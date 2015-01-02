# vim: set fileencoding=utf-8 :

# Copyright (C) 2008 Joao Paulo de Souza Medeiros.
#
# Author(s): João Paulo de Souza Medeiros <ignotus21@gmail.com>
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
import pango
import bestwidgets as bw



class Command(bw.BWExpander):
    """
    """
    def __init__(self, send_function, parse_function):
        """
        """
        bw.BWExpander.__init__(self, "Command")
        self.bw_no_padding()
        self.set_border_width(6)
        self.set_expanded(True)

        self.__send_command = send_function
        self.__parse_function = parse_function

        self.__font = pango.FontDescription('Monospace')

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__table = bw.BWTable(2, 3)
        self.__table.bw_set_spacing(6)

        self.__icon = gtk.Image()
        self.__icon.set_from_stock(gtk.STOCK_SELECT_FONT,
                                   gtk.ICON_SIZE_LARGE_TOOLBAR)

        self.__entry = gtk.Entry()
        self.__entry.connect('changed', self.__entry_changed)
        self.__entry.connect('key_press_event', self.__entry_key_press)
        self.__entry.modify_font(self.__font)

        self.__button = gtk.ToggleButton("History")
        self.__button.connect("toggled", self.__show_history)
        self.__button_image = gtk.Image()
        self.__button_image.set_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_MENU)
        self.__button.set_image(self.__button_image)
        self.__button.set_sensitive(False)

        self.__history = bw.BWTextEditor()
        self.__history.bw_set_editable(False)
        self.__history.set_border_width(0)
        self.__history.bw_modify_font(self.__font)
        self.__history.hide_all()
        self.__history.set_no_show_all(True)
        self.__history.bw_set_scroll(True)

        self.__table.bw_attach_next(self.__icon, gtk.FILL, gtk.FILL)
        self.__table.bw_attach_next(self.__entry)
        self.__table.bw_attach_next(self.__button, gtk.FILL, gtk.FILL)
        self.__table.attach(self.__history, 0, 3, 1, 2)

        self.bw_add(self.__table)


    def __show_history(self, widget):
        """
        """
        if self.__button.get_active():

            self.__history.set_no_show_all(False)
            self.__history.show_all()

        else:

            self.__history.hide_all()
            self.__history.set_no_show_all(True)


    def __entry_changed(self, widget):
        """
        """
        command = self.__entry.get_text().strip()

        if self.__parse_function(command):
            self.__icon.set_from_stock(gtk.STOCK_APPLY,
                                       gtk.ICON_SIZE_LARGE_TOOLBAR)

        else:
            self.__icon.set_from_stock(gtk.STOCK_SELECT_FONT,
                                       gtk.ICON_SIZE_LARGE_TOOLBAR)


    def __entry_key_press(self, widget, event):
        """
        """
        key = gtk.gdk.keyval_name(event.keyval)

        if key == "Return" or key == "KP_Enter":
            self.__send_command(self.__entry.get_text().strip())



    def add_text(self, text):
        """
        """
        self.__button.set_sensitive(True)
        self.__history.bw_set_text("\n".join([self.__history.bw_get_text(),
                                              text]).strip())


    def set_status_icon(self, value):
        """
        """
        if value:
            self.__icon.set_from_stock(gtk.STOCK_YES,
                                       gtk.ICON_SIZE_LARGE_TOOLBAR)

        else:
            self.__icon.set_from_stock(gtk.STOCK_NO,
                                       gtk.ICON_SIZE_LARGE_TOOLBAR)
