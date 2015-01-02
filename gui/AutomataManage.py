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

import os
import gtk
import pango
import pydot
import types
import bestwidgets as bw

from gui.Canvas import Canvas
from gui.Image import Pixmaps
from gui.Command import Command
from core.Path import path
from core.Automaton import *
from core.Parser import Parser


TMP_IMAGE = 'share/pixmaps/drawing.png'

GRAPH_ATTR = {'rankdir':  'LR',
              'fontsize': '10',
              'fontname': 'Monospaced Bold'}

NODE_ATTR = {'shape':    'circle',
             'fontsize': '10',
             'fontname': 'Monospaced Bold'}

START_NODE_ATTR = {'style':     'filled',
                   'fillcolor': '#000000',
                   'fontcolor': '#ffffff'}

FINAL_NODE_ATTR = {'shape': 'doublecircle'}

EDGE_ATTR = {'color':    '#888888',
             'fontsize': '10',
             'fontname': 'Monospaced'}

TRANSITION_TEXT = "(%s . %s) -> %s"
LAMBDA_TRANSITION_TEXT = "(%s . &) -> %s"



class AutomataManage(bw.BWVBox):
    """
    """
    def __init__(self):
        """
        """
        bw.BWVBox.__init__(self, spacing=2)
        self.set_sensitive(False)

        self.__parser = Parser()

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__automaton_list = AutomatonList(self)
        self.__automaton_view = AutomatonView()
        self.__command = Command(self.execute_command,
                                 self.parse_command)

        self.bw_pack_start_noexpand_nofill(self.__automaton_list)
        self.bw_pack_start_expand_fill(self.__automaton_view)
        self.bw_pack_start_noexpand_nofill(self.__command)


    def show_automaton_details(self, value):
        """
        """
        self.__automaton_view.show_details(value)


    def refresh_view(self, widget=None):
        """
        """
        self.__automaton_view.refresh_view()


    def clear(self):
        """
        """
        self.__automaton_view.clear()


    def set_automaton(self, automaton):
        """
        """
        self.__automaton_view.set_automaton(automaton)


    def create_new_automaton(self):
        """
        """
        if self.__automaton_list.get_number_of_automata() == 0:
            self.set_sensitive(True)

        return self.__automaton_list.create_new_automaton()


    def create_automaton_from_xml(self, file):
        """
        """
        result, argument = get_automaton_from_xml(file)

        if result:
            if self.__automaton_list.get_number_of_automata() == 0:
                self.set_sensitive(True)

            self.__automaton_list.append_automaton(argument)

        return result, argument


    def write_automaton_to_xml(self, file):
        """
        """
        automaton = self.__automaton_list.get_selected_automaton()

        result, argument = save_automaton_to_xml(automaton, file)

        return result, argument


    def get_selected_automaton(self):
        """
        """
        return self.__automaton_list.get_selected_automaton()


    def parse_command(self, command):
        """
        """
        return self.__parser.parse(command)


    def execute_command(self, command):
        """
        """
        automaton = self.__automaton_list.get_selected_automaton()

        if self.__parser.parse(command) and automaton != None:

            result = self.__parser.execute_command(automaton, command)

            if result:

                self.__command.add_text(command)
                self.__command.set_status_icon(True)

                self.__automaton_view.refresh_view()

                if type(result) == types.InstanceType:
                    self.__automaton_list.append_automaton(result)

                return True

        self.__command.set_status_icon(False)

        return False



class AutomatonView(gtk.HPaned):
    """
    """
    def __init__(self, automaton=None):
        """
        """
        gtk.HPaned.__init__(self)

        self.__automaton = automaton
        self.__pixmap = Pixmaps()

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__hbox = bw.BWHBox()

        self.__canvas = Canvas()

        self.__details = AutomatonDetails()

        self.add1(self.__canvas)
        self.add2(self.__details)

        self.__details.hide_all()
        self.__details.set_no_show_all(True)


    def show_details(self, value):
        """
        """
        if value:
            self.__details.set_no_show_all(False)
            self.__details.show_all()
            self.__details.set_size_request(200, -1)
            self.set_position(450)

        else:
            self.__details.hide_all()
            self.__details.set_no_show_all(True)


    def clear(self):
        """
        """
        self.__canvas.set_image(None)
        self.__details.clear()


    def set_automaton(self, automaton):
        """
        """
        self.__automaton = automaton
        self.__details.set_automaton(self.__automaton)

        self.refresh_view()


    def refresh_view(self):
        """
        """
        file_url = os.path.join(path.get_dirbase(), TMP_IMAGE)

        self.create_dot_object().write_png(file_url, prog="dot")

        self.__canvas.set_image(self.__pixmap.get_pixbuf('drawing', force=True))
        self.__details.refresh()


    def create_dot_object(self):
        """
        """
        graph = pydot.Dot()
        graph.set_label(self.__automaton.get_name())

        states = self.__automaton.get_states()
        events = self.__automaton.get_events()
        transitions = self.__automaton.get_transitions()
        lambda_transitions = self.__automaton.get_lambda_transitions()

        start_state = self.__automaton.get_start_state()
        final_states = self.__automaton.get_final_states()

        # add graph attributes
        for key in GRAPH_ATTR.keys():
            graph.set(key, GRAPH_ATTR[key])

        # add nodes to graph and set its attributes
        for s in states:

            graph.add_node(pydot.Node(s))
            node = graph.get_node(s)[0]

            for key in NODE_ATTR.keys():
                node.set(key, NODE_ATTR[key])

        # add edges to graph
        for (a, e) in transitions.keys():

            for n in transitions[(a, e)]:

                edge = pydot.Edge(a, n, label=e)
            
                for key in EDGE_ATTR.keys():
                    edge.set(key, EDGE_ATTR[key])

                graph.add_edge(edge)

        # add edges to graph (lambda)
        for a in lambda_transitions.keys():

            for n in lambda_transitions[a]:

                edge = pydot.Edge(a, n, label='&')
            
                for key in EDGE_ATTR.keys():
                    edge.set(key, EDGE_ATTR[key])

                graph.add_edge(edge)

        # set final states attributes
        for s in final_states:

            node = graph.get_node(s)[0]

            for key in FINAL_NODE_ATTR.keys():
                node.set(key, FINAL_NODE_ATTR[key])

        # set initial state attributes
        if start_state != None:

            start_node = graph.get_node(start_state)[0]

            for key in START_NODE_ATTR.keys():
                start_node.set(key, START_NODE_ATTR[key])

        return graph



class AutomatonList(bw.BWHBox):
    """
    """
    def __init__(self, manage):
        """
        """
        bw.BWHBox.__init__(self, spacing=2)
        self.set_border_width(2)

        self.__parser = Parser()

        self.__manage = manage
        self.__automata = []
        self.__last_automaton = None

        self.__font = pango.FontDescription('Monospace')

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__label = bw.BWSectionLabel('Select:')

        self.__list = bw.BWChangeableComboBoxEntry()
        self.__list.connect("changed", self.__list_changed)
        self.__list.child.connect("changed", self.__name_changed)
        self.__list.child.connect("key_press_event", self.__key_pressed)
        self.__list.modify_font(self.__font)

        self.__show_button = bw.BWToggleStockButton(gtk.STOCK_INFO)
        self.__show_button.connect("clicked", self.__show_data)

        self.__refresh_button = bw.BWStockButton(gtk.STOCK_REFRESH)
        self.__refresh_button.connect("clicked", self.__manage.refresh_view)

        self.__close_button = bw.BWStockButton(gtk.STOCK_CLOSE)
        self.__close_button.connect("clicked", self.__close_view)

        self.bw_pack_start_noexpand_nofill(self.__label)
        self.bw_pack_start_expand_fill(self.__list)
        self.bw_pack_start_noexpand_nofill(self.__show_button)
        self.bw_pack_start_noexpand_nofill(self.__refresh_button)
        self.bw_pack_start_noexpand_nofill(self.__close_button)


    def __close_view(self, widget):
        """
        """
        active = self.__list.bw_get_active()

        del self.__automata[active]
        self.__list.remove_text(active)

        if len(self.__automata) == 0:

            self.__manage.clear()
            self.__manage.set_sensitive(False)
            self.__list.child.set_text("")

        else:

            new_index = (active, active - 1)[active > 0]

            self.__last_automaton = self.__automata[new_index]
            self.__list.set_active(new_index)
            self.__manage.set_automaton(self.__last_automaton)


    def __show_data(self, widget):
        """
        """
        self.__manage.show_automaton_details(self.__show_button.get_active())


    def __key_pressed(self, widget, event):
        """
        """
        key = gtk.gdk.keyval_name(event.keyval)

        if key == "Return" or key == "KP_Enter":
            self.__manage.refresh_view()


    def __list_changed(self, widget):
        """
        """
        active = self.__list.bw_get_active()

        if len(self.__automata) > active and\
           self.__automata[active] != self.__last_automaton:

            automaton = self.__automata[active]

            self.__last_automaton = automaton
            self.__manage.set_automaton(automaton)


    def __name_changed(self, widget):
        """
        """
        if len(self.__automata) > 0:

            automaton = self.__automata[self.__list.bw_get_active()]
            automaton.set_name(widget.get_text())


    def create_new_automaton(self):
        """
        """
        self.__automata.append(Automaton())
        self.__manage.set_automaton(self.__automata[-1])

        self.__list.append_text(self.__automata[-1].get_name())
        self.__list.set_active(len(self.__automata) - 1)

        return True


    def append_automaton(self, automaton):
        """
        """
        self.__automata.append(automaton)
        self.__manage.set_automaton(self.__automata[-1])

        self.__list.append_text(self.__automata[-1].get_name())
        self.__list.set_active(len(self.__automata) - 1)

        return True


    def get_selected_automaton(self):
        """
        """
        return self.__last_automaton


    def get_number_of_automata(self):
        """
        """
        return len(self.__automata)



class AutomatonDetails(bw.BWTable):
    """
    """
    def __init__(self):
        """
        """
        bw.BWTable.__init__(self, 10, 1)
        self.bw_set_spacing(0)
        self.set_border_width(0)

        self.__automaton = None

        self.__font = pango.FontDescription('Monospace')

        self.__create_widgets()


    def __create_widgets(self):
        """
        """
        self.__name = bw.BWFrame("Name")
        self.__name_value = bw.BWLabel()
        self.__name_value.set_line_wrap(True)
        self.__name_value.set_selectable(True)
        self.__name.bw_add(self.__name_value)

        self.__comment = bw.BWFrame("Comment")
        self.__comment_value = bw.BWTextView()
        self.__comment_value.set_border_width(0)
        self.__comment_value.bw_set_wrap_mode(gtk.WRAP_WORD)
        self.__comment_value.bw_get_textbuffer().connect("changed",
                                                         self.__change_comment)
        self.__comment.bw_add(self.__comment_value)

        self.__states = bw.BWFrame("States")
        self.__states_value = bw.BWTextEditor()
        self.__states_value.set_border_width(0)
        self.__states_value.bw_modify_font(self.__font)
        self.__states_value.bw_set_editable(False)
        self.__states.bw_add(self.__states_value)

        self.__events = bw.BWFrame("Events")
        self.__events_value = bw.BWTextEditor()
        self.__events_value.set_border_width(0)
        self.__events_value.bw_modify_font(self.__font)
        self.__events_value.bw_set_editable(False)
        self.__events.bw_add(self.__events_value)

        self.__transitions = bw.BWFrame("Transitions")
        self.__transitions_value = bw.BWTextEditor()
        self.__transitions_value.set_border_width(0)
        self.__transitions_value.bw_modify_font(self.__font)
        self.__transitions_value.bw_set_editable(False)
        self.__transitions.bw_add(self.__transitions_value)

        self.bw_attach_next(self.__name, gtk.FILL, gtk.FILL)
        self.bw_attach_next(self.__comment)
        self.bw_attach_next(self.__states)
        self.bw_attach_next(self.__events)
        self.bw_attach_next(self.__transitions)


    def __change_comment(self, widget):
        """
        """
        if self.__automaton != None:
            self.__automaton.set_comment(self.__comment_value.bw_get_text())


    def set_automaton(self, automaton):
        """
        """
        self.__automaton = automaton


    def clear(self):
        """
        """
        self.__name_value.set_text('')
        self.__comment_value.bw_set_text('')
        self.__states_value.bw_set_text('')
        self.__events_value.bw_set_text('')
        self.__transitions_value.bw_set_text('')


    def refresh(self):
        """
        """
        if self.__automaton != None:

            # setting name
            self.__name_value.set_text(self.__automaton.get_name())

            # setting comment
            self.__comment_value.bw_set_text(self.__automaton.get_comment())

            # setting states
            states = self.__automaton.get_states()

            if len(states) > 0:

                states_text = []

                for state in states:

                    text = state
                    flag = []

                    if state == self.__automaton.get_start_state():
                        flag.append("init")

                    if state in self.__automaton.get_final_states():
                        flag.append("mark")

                    if len(flag) > 0:
                        text += " (%s)" % ", ".join(flag)

                    states_text.append(text)

                self.__states_value.bw_set_text('\n'.join(states_text))

            else:
                self.__states_value.bw_set_text('')

            # setting states
            events = self.__automaton.get_events()

            if len(events) > 0:
                self.__events_value.bw_set_text('\n'.join(events))

            else:
                self.__events_value.bw_set_text('')

            # setting transitions
            lambda_transitions = self.__automaton.get_lambda_transitions()
            transitions = self.__automaton.get_transitions()

            if len(lambda_transitions) > 0 or len(transitions) > 0:

                text = []

                for a in lambda_transitions.keys():
                    
                    for n in lambda_transitions[a]:
                        text.append(LAMBDA_TRANSITION_TEXT % (a, n))

                for (a, e) in transitions.keys():
                    
                    for n in transitions[(a, e)]:
                        text.append(TRANSITION_TEXT % (a, e, n))

                self.__transitions_value.bw_set_text('\n'.join(text))

            else:
                self.__transitions_value.bw_set_text('')
