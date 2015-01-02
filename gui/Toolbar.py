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

import bestwidgets as bw
from gui.Dialogs import AboutDialog


FILE_OPEN_BUTTONS = (gtk.STOCK_CANCEL,
                     gtk.RESPONSE_CANCEL,
                     gtk.STOCK_OPEN,
                     gtk.RESPONSE_OK)

FILE_SAVE_BUTTONS = (gtk.STOCK_CANCEL,
                     gtk.RESPONSE_CANCEL,
                     gtk.STOCK_SAVE,
                     gtk.RESPONSE_OK)



class Toolbar(gtk.Toolbar):
    """
    """
    def __init__(self, window):
        """
        """
        gtk.Toolbar.__init__(self)
        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        self.set_tooltips(True)

        self.__window = window

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__tooltips = gtk.Tooltips()

        self.__new = gtk.ToolButton(gtk.STOCK_NEW)
        self.__new.set_label('New')
        self.__new.set_is_important(True)
        self.__new.connect('clicked', self.__new_callback)

        self.__open = gtk.ToolButton(gtk.STOCK_OPEN)
        self.__open.set_label('Open')
        self.__open.set_is_important(True)
        self.__open.connect('clicked', self.__open_callback)

        self.__save = gtk.ToolButton(gtk.STOCK_SAVE)
        self.__save.set_label('Save')
        self.__save.set_is_important(True)
        self.__save.connect('clicked', self.__save_callback)

        self.__save_as = gtk.ToolButton(gtk.STOCK_SAVE_AS)
        self.__save_as.set_label('Save as')
        self.__save_as.set_is_important(True)
        self.__save_as.connect('clicked', self.__save_callback, True)

        self.__fullscreen = gtk.ToggleToolButton(gtk.STOCK_FULLSCREEN)
        self.__fullscreen.set_label('Fullscreen')
        self.__fullscreen.set_is_important(True)
        self.__fullscreen.connect('clicked', self.__fullscreen_callback)
        self.__fullscreen.set_tooltip(self.__tooltips, 'Toggle fullscreen')

        self.__about = gtk.ToolButton(gtk.STOCK_ABOUT)
        self.__about.set_label('About')
        self.__about.set_is_important(True)
        self.__about.connect('clicked', self.__about_callback)
        self.__about.set_tooltip(self.__tooltips, 'About RadialNet')

        self.__expander = gtk.SeparatorToolItem()
        self.__expander.set_expand(True)
        self.__expander.set_draw(False)

        self.insert(self.__new,         0)
        self.insert(self.__open,        1)
        self.insert(self.__save,        2)
        self.insert(self.__save_as,     3)
        self.insert(self.__expander,    4)
        self.insert(self.__fullscreen,  5)
        self.insert(self.__about,       6)


    def set_empty_state(self, value):
        """
        """
        if value:
            self.__save.set_sensitive(False)
            self.__save_as.set_sensitive(False)

        else:
            self.__save.set_sensitive(True)
            self.__save_as.set_sensitive(True)


    def __new_callback(self, widget=None):
        """
        """
        self.__window.new_button_action()


    def __open_callback(self, widget=None):
        """
        """
        self.__chooser = gtk.FileChooserDialog('Open file',
                                               None,
                                               gtk.FILE_CHOOSER_ACTION_OPEN,
                                               FILE_OPEN_BUTTONS)
        self.__chooser.set_keep_above(True)

        if self.__chooser.run() == gtk.RESPONSE_OK:
            self.__window.open_button_action(self.__chooser.get_filename())

        self.__chooser.destroy()


    def __save_callback(self, widget=None, save_as=False):
        """
        """
        result = self.__window.is_saved()

        if result == False or save_as:

            self.__chooser = gtk.FileChooserDialog('Save file',
                                                   None,
                                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                                   FILE_SAVE_BUTTONS)
            self.__chooser.set_keep_above(True)

            if self.__chooser.run() == gtk.RESPONSE_OK:
                self.__window.save_button_action(self.__chooser.get_filename())

            self.__chooser.destroy()

        else:
            self.__window.save_button_action(result)


    def __control_callback(self, widget=None):
        """
        """
        if self.__control.get_active() != self.__state['control']:

            if self.__control.get_active():
                self.__control_widget.show()

            else:
                self.__control_widget.hide()

            self.__state['control'] = self.__control.get_active()


    def __fullscreen_callback(self, widget=None):
        """
        """
        if self.__fullscreen.get_active():
            self.__window.fullscreen()

        else:
            self.__window.unfullscreen()


    def __about_callback(self, widget):
        """
        """
        self.__about_dialog = AboutDialog()
        self.__about_dialog.show_all()
