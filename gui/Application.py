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
import gobject
import bestwidgets as bw

from gui.Toolbar import Toolbar
from gui.Dialogs import AboutDialog
from gui.Image import Pixmaps
from gui.AutomataManage import AutomataManage
from core.Info import INFO


DIMENSION = (640, 480)



class Application(bw.BWMainWindow):
    """
    """
    def __init__(self):
        """
        """
        bw.BWMainWindow.__init__(self)
        self.set_default_size(DIMENSION[0], DIMENSION[1])
        self.set_title("%s %s" % (INFO['name'], INFO['version']))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_icon(Pixmaps().get_pixbuf('logo'))

        self.__file_list = dict()

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__vbox = bw.BWVBox(spacing=1)

        self.__toolbar = Toolbar(self)
        self.__automata_manage = AutomataManage()
        self.__statusbar = bw.BWStatusbar()

        self.__vbox.bw_pack_start_noexpand_nofill(self.__toolbar)
        self.__vbox.bw_pack_start_expand_fill(self.__automata_manage)
        self.__vbox.bw_pack_start_noexpand_nofill(self.__statusbar)

        self.__toolbar.set_empty_state(True)

        self.add(self.__vbox)
        self.show_all()
        self.connect('destroy', gtk.main_quit)


    def is_saved(self):
        """
        """
        automaton = self.__automata_manage.get_selected_automaton()
        
        if automaton in self.__file_list.keys():
            return self.__file_list[automaton]

        return False


    def new_button_action(self):
        """
        """
        if self.__automata_manage.create_new_automaton():
            self.__toolbar.set_empty_state(False)


    def open_button_action(self, file):
        """
        """
        result, argument = self.__automata_manage.create_automaton_from_xml(file)

        if result:

            self.__toolbar.set_empty_state(False)
            self.__file_list[argument] = file

        else:
            alert = bw.BWAlertDialog(self,
                                     primary_text='Error opening file.',
                                     secondary_text=argument)

            alert.show_all()


    def save_button_action(self, file):
        """
        """
        result, argument = self.__automata_manage.write_automaton_to_xml(file)

        if result:

            self.__toolbar.set_empty_state(False)
            self.__file_list[argument] = file

        else:
            alert = bw.BWAlertDialog(self,
                                     primary_text='Error saving file.',
                                     secondary_text=argument)

            alert.show_all()


    def start(self):
        """
        """
        gtk.main()
