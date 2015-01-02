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

import re

from core.XMLHandler import XMLReader, XMLWriter, XMLNode


STATE_RE = "^[\w]+(,[\w])*$"
EVENT_RE = "^[\w]+$"

ERROR = {"OPEN":       "Error opening file \"%s\".",
         "PARSE":      "Error parsing file \"%s\".",
         "WRITE":      "Error writing file \"%s\".",
         "INVALID":    "Error validating automaton.",
         "STATE":      "Error inserting state \"%s\".",
         "EVENT":      "Error inserting event \"%s\".",
         "LAMBDA":     "Error inserting lambda transition \"%s\" > \"%s\".",
         "TRANSITION": "Error inserting transition (\"%s\", \"%s\") > \"%s\"."}



def save_automaton_to_xml(automaton, file):
    """
    """
    if not automaton.validate():
        return False, ERROR["INVALID"]

    try:
        writer = XMLWriter(open(file, 'w'))

    except:
        return False, (ERROR["OPEN"] % xml_file)

    root = XMLNode("automaton")
    root.add_attr("name", automaton.get_name())
    root.add_attr("start", automaton.get_start_state())

    xml_states = XMLNode("states")

    for state in automaton.get_states():

        xml_state = XMLNode("state")
        xml_state.add_attr("name", state)

        if state in automaton.get_final_states():
            xml_state.add_attr("option", "final")

        xml_states.add_child(xml_state)

    root.add_child(xml_states)

    xml_events = XMLNode("events")

    for event in automaton.get_events():

        xml_event = XMLNode("event")
        xml_event.add_attr("name", event)

        xml_events.add_child(xml_event)

    root.add_child(xml_events)

    xml_lambda_transitions = XMLNode("lambdas")

    for transition in automaton.get_lambda_transitions().keys():

        state_from = transition
        states_to = automaton.get_lambda_transitions()[transition]

        for state_to in states_to:

            xml_lambda_transition = XMLNode("lambda")
            xml_lambda_transition.add_attr("from", state_from)
            xml_lambda_transition.add_attr("to", state_to)

            xml_lambda_transitions.add_child(xml_lambda_transition)

    root.add_child(xml_lambda_transitions)

    xml_transitions = XMLNode("transitions")

    for transition in automaton.get_transitions().keys():

        state_from, event = transition
        states_to = automaton.get_transitions()[transition]

        for state_to in states_to:

            xml_transition = XMLNode("transition")
            xml_transition.add_attr("from", state_from)
            xml_transition.add_attr("to", state_to)
            xml_transition.add_attr("when", event)

            xml_transitions.add_child(xml_transition)

    root.add_child(xml_transitions)

    xml_comment = XMLNode("comment")
    xml_comment.set_text(automaton.get_comment())

    root.add_child(xml_comment)

    try:

        writer.set_root(root)
        writer.write()

    except:
        return False, ERROR["WRITE"]

    return True, automaton


def get_automaton_from_xml(xml_file):
    """
    """
    try:
        parser = XMLReader(xml_file)

    except:
        return False, (ERROR["OPEN"] % xml_file)

    try:
        parser.parse()

    except:
        return False, (ERROR["PARSE"] % xml_file)

    automaton = Automaton()

    xml_automaton = parser.get_root()

    automaton.set_name(xml_automaton.get_attr("name"))

    # getting states
    xml_states_node = xml_automaton.search_children("states", True)

    if xml_states_node != None:

        xml_states = xml_states_node.get_children()

        for xml_state in xml_states:

            state_name = xml_state.get_attr("name")
            result = automaton.add_state(state_name)

            if not result:
                return False, (ERROR["STATE"] % state_name)

            if xml_state.get_attr("option") != None:

                if xml_state.get_attr("option") == "final":
                    automaton.add_final_state(state_name)

    automaton.set_start_state(xml_automaton.get_attr("start"))

    # getting events
    xml_events_node = xml_automaton.search_children("events", True)

    if xml_events_node != None:

        xml_events = xml_events_node.get_children()

        for xml_event in xml_events:

            event_name = xml_event.get_attr("name")
            result = automaton.add_event(event_name)

            if not result:
                return False, (ERROR["EVENT"] % event_name)

    # getting lambda transitions
    xml_lambda_transitions_node = xml_automaton.search_children("lambdas", True)

    if xml_lambda_transitions_node != None:

        xml_lambda_transitions = xml_lambda_transitions_node.get_children()

        for xml_lambda_transition in xml_lambda_transitions:

            state_from = xml_lambda_transition.get_attr("from")
            state_to = xml_lambda_transition.get_attr("to")

            result = automaton.add_lambda(state_from, state_to)

            if not result:
                return False, (ERROR["LAMBDA"] % (state_from, state_to))

    # getting transitions
    xml_transitions_node = xml_automaton.search_children("transitions", True)

    if xml_transitions_node != None:

        xml_transitions = xml_transitions_node.get_children()

        for xml_transition in xml_transitions:

            state_from = xml_transition.get_attr("from")
            state_to = xml_transition.get_attr("to")
            event = xml_transition.get_attr("when")

            result = automaton.add_transition(state_from, event, state_to)

            if not result:
                return False, (ERROR["TRANSITION"] % (state_from,
                                                      event,
                                                      state_to))

    # getting comment
    xml_comment_node = xml_automaton.search_children("comment", True)
    automaton.set_comment(xml_comment_node.get_text())

    return True, automaton




class Automaton:
    """
    """
    def __init__(self, name="<unnamed>"):
        """
        """
        self.__name = name
        self.__states = set()
        self.__events = set()
        self.__lambda = dict()
        self.__transitions = dict()
        self.__start_state = None
        self.__final_states = set()
        self.__comment = "<uncommented>"


    def add_state(self, state):
        """
        """
        if re.search(STATE_RE, state) and state not in self.__states:

            self.__states.add(state)
            return True

        return False


    def del_state(self, state):
        """
        """
        if re.search(STATE_RE, state) and state in self.__states:

            for t in self.__transitions.keys():

                if state == t[0] or state == self.__transitions[t]:
                    self.__transitions.pop(t)

            if state == self.__start_state:
                self.__start_state = None

            if state in self.__final_states:
                self.__final_states.remove(state)

            self.__states.remove(state)

            return True

        return False


    def add_event(self, event):
        """
        """
        if re.search(EVENT_RE, event) and event not in self.__events:

            self.__events.add(event)
            return True

        return False


    def del_event(self, event):
        """
        """
        if re.search(EVENT_RE, event) and event in self.__events:

            for t in self.__transitions.keys():

                if event == t[1]:
                    self.__transitions.pop(t)

            self.__events.remove(event)

            return True

        return False


    def add_lambda(self, a_state, n_state):
        """
        """
        test_as = re.search(STATE_RE, a_state) and a_state in self.__states
        test_ns = re.search(STATE_RE, n_state) and n_state in self.__states

        exists = self.__lambda.has_key(a_state)

        if exists:
            exists = self.__lambda[a_state] == n_state

        else:
            self.__lambda[a_state] = set()

        if test_as and test_ns and not exists:

            self.__lambda[a_state].add(n_state)
            return True

        return False


    def del_lambda(self, a_state, n_state):
        """
        """
        test_as = re.search(STATE_RE, a_state) and a_state in self.__states
        test_ns = re.search(STATE_RE, n_state) and n_state in self.__states

        exists = self.__lambda.has_key(a_state)

        if exists:
            exists = self.__lambda[a_state] == n_state

        if test_as and test_ns and exists:

            if len(self.__lambda[a_state]) == 1:
                self.__lambda.pop(a_state)

            else:
                self.__lambda[a_state].pop(n_state)

            return True

        return False


    def add_transition(self, a_state, event, n_state):
        """
        """
        test_as = re.search(STATE_RE, a_state) and a_state in self.__states
        test_ns = re.search(STATE_RE, n_state) and n_state in self.__states
        test_sy = re.search(EVENT_RE, event) and event in self.__events

        exists = self.__transitions.has_key((a_state, event))

        if exists:
            exists = self.__transitions[(a_state, event)] == n_state

        else:
            self.__transitions[(a_state, event)] = set()

        if test_as and test_ns and test_sy and not exists:

            self.__transitions[(a_state, event)].add(n_state)
            return True

        return False


    def del_transition(self, a_state, event, n_state):
        """
        """
        test_as = re.search(STATE_RE, a_state) and a_state in self.__states
        test_ns = re.search(STATE_RE, n_state) and n_state in self.__states
        test_sy = re.search(EVENT_RE, event) and event in self.__events

        exists = self.__transitions.has_key((a_state, event))

        if exists:
            exists = self.__transitions[(a_state, event)] == n_state

        if test_as and test_ns and test_sy and exists:

            if len(self.__transitions[(a_state, event)]) == 1:
                self.__transitions.pop((a_state, event))

            else:
                self.__transitions[(a_state, event)].pop(n_state)

            return True

        return False


    def set_start_state(self, state):
        """
        """
        if re.search(STATE_RE, state) and\
           state in self.__states and\
           state != self.__start_state:

            self.__start_state = state
            return True

        return False


    def add_final_state(self, state):
        """
        """
        if re.search(STATE_RE, state) and\
           state in self.__states and\
           state not in self.__final_states:

            self.__final_states.add(state)
            return True

        return False


    def del_final_state(self, state):
        """
        """
        if re.search(STATE_RE, state) and state in self.__final_states:

            self.__final_states.remove(state)
            return True

        return False


    def set_name(self, name):
        """
        """
        self.__name = name


    def get_name(self):
        """
        """
        return self.__name


    def get_states(self):
        """
        """
        return self.__states


    def get_events(self):
        """
        """
        return self.__events


    def get_lambda_transitions(self):
        """
        """
        return self.__lambda


    def get_transitions(self):
        """
        """
        return self.__transitions


    def get_start_state(self):
        """
        """
        return self.__start_state


    def get_final_states(self):
        """
        """
        return self.__final_states


    def set_comment(self, comment):
        """
        """
        self.__comment = comment


    def get_comment(self):
        """
        """
        return self.__comment


    def lambda_closure(self, state=None):
        """
        """
        if state == None:
            state = self.__start_state

        if state in self.__lambda.keys():
            return list(self.__lambda[state].union([state]))

        return [state]


    def move(self, state, event):
        """
        """
        if (state, event) in self.__transitions.keys():
            return self.__transitions[(state, event)]

        return []


    def validate(self):
        """
        """
        has_start_state = self.__start_state != None
        has_final_state = len(self.__final_states) > 0
        has_at_least_one_state = len(self.__states) > 0
        has_at_least_one_event = len(self.__events) > 0
        has_at_least_one_transition = len(self.__transitions) > 0

        if has_start_state and\
           has_final_state and\
           has_at_least_one_state and\
           has_at_least_one_event and\
           has_at_least_one_transition:
               return True

        return False




if __name__ == "__main__":

    a = Automaton()

    a.add_state('A')
    a.add_state('B')
    a.add_state('C')

    a.add_event('a')
    a.add_event('b')

    a.add_transition('A', 'a', 'B')
    a.add_transition('A', 'b', 'C')
    a.add_transition('B', 'a', 'B')
    a.add_transition('B', 'b', 'C')
    a.add_transition('C', 'a', 'C')
    a.add_transition('C', 'b', 'B')

    a.add_final_state('B')
    a.set_start_state('A')
