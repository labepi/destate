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

import os
import sys



class Path:
    """
    """
    def __init__(self, dirbase):
        """
        """
        self.__dirbase = dirbase


    def get_dirbase(self):
        """
        """
        return self.__dirbase


path = Path(os.path.dirname(sys.argv[0]))
