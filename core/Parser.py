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

from core.Automaton import STATE_RE, EVENT_RE
from core.Operations import NFA2DFA


LAMBDA_ARG = (STATE_RE[1:-1], STATE_RE[1:-1])
TRANS_ARG = (STATE_RE[1:-1], EVENT_RE[1:-1], STATE_RE[1:-1])

RE = list()

RE.append("^do[\s]+(nfa2dfa)$")
RE.append("^(add|del)[\s]+(state)[\s]+(%s)$" % STATE_RE[1:-1])
RE.append("^(add|del)[\s]+(event)[\s]+(%s)$" % EVENT_RE[1:-1])
RE.append("^(add|del)[\s]+(lambda)[\s]+(%s)[\s]+(%s)$" % LAMBDA_ARG)
RE.append("^(add|del)[\s]+(transition)[\s]+(%s)[\s]+(%s)[\s]+(%s)$" % TRANS_ARG)
RE.append("^(init|mark|unmark)[\s]+(%s)$" % STATE_RE[1:-1])



class Parser:
    """
    """
    def parse(self, string):
        """
        """
        for e in RE:

            if re.match(e, string) != None:
                return True

        return False


    def execute_command(self, automaton, string):
        """
        """
        arguments = string.split()
        command = arguments[0]

        if command == "add":

            element = arguments[1]

            if element == "state":
                return automaton.add_state(arguments[2])

            if element == "event":
                return automaton.add_event(arguments[2])

            if element == "lambda":
                return automaton.add_lambda(arguments[2],
                                            arguments[3])

            if element == "transition":
                return automaton.add_transition(arguments[2],
                                                arguments[3],
                                                arguments[4])

        if command == "del":

            element = arguments[1]

            if element == "state":
                return automaton.del_state(arguments[2])

            if element == "event":
                return automaton.del_event(arguments[2])

            if element == "lambda":
                return automaton.del_lambda(arguments[2],
                                            arguments[3])

            if element == "transition":
                return automaton.del_transition(arguments[2],
                                                arguments[3],
                                                arguments[4])

        if command == "init":
            return automaton.set_start_state(arguments[1])

        if command == "mark":
            return automaton.add_final_state(arguments[1])

        if command == "unmark":
            return automaton.del_final_state(arguments[1])

        if command == "do":

            operation = arguments[1]

            if operation == "nfa2dfa":

                if automaton.validate():

                    o = NFA2DFA(automaton)
                    return o.execute()

                return False
