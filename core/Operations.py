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

from core.Automaton import Automaton


class NFA2DFA:
    """
    """
    def __init__(self, nfa=None):
        """
        """
        self.__nfa = nfa


    def set_nfa(self, nfa):
        """
        """
        self.__nfa = nfa


    def execute(self):
        """
        """
        if self.__nfa != None:

            start_state = self.__nfa.lambda_closure()
            start_state.sort()

            states = list()
            transitions = list()

            new_states = [start_state]

            # applying the subset algorithm
            while len(new_states) > 0:

                new_states_list = list()
                state = new_states.pop()

                for e in self.__nfa.get_events():

                    s = set()

                    for a in state:
                        s.update(self.__nfa.move(a, e))

                    if len(s) > 0:

                        t = set()

                        for a in s:
                            t.update(self.__nfa.lambda_closure(a))

                        s.update(t)

                        s = list(s)
                        s.sort()

                        transitions.append(((state, e), s))

                        if s not in new_states_list:
                            new_states_list.append(s)

                states.append(state)

                for new_state in new_states_list:
                    if new_state not in states:
                        new_states.append(new_state)

            # construct new dfa automaton
            dfa = Automaton()

            for state in states:

                dfa.add_state("_".join(state))

                for s in state:

                    if s in self.__nfa.get_final_states():

                        dfa.add_final_state("_".join(state))
                        break

            dfa.set_start_state("_".join(start_state))

            for ((s, e), n) in transitions:

                dfa.add_event(e)
                dfa.add_transition("_".join(s),
                                   e,
                                   "_".join(n))

            return dfa

        return None



if __name__ == "__main__":

    from core.Automaton import save_automaton_to_xml, get_automaton_from_xml
    import sys

    c = NFA2DFA(get_automaton_from_xml(sys.argv[1])[1])
    save_automaton_to_xml(c.execute(), sys.argv[2])
