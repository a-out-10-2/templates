#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#   <بعض المرافق>
#
#   Copyright © <YYYY> Andrew Moe
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. Or, see
#   <http://www.gnu.org/licenses/gpl-2.0.html>.
# -----------------------------------------------------------------------------
import sys
from mpi4py import MPI

__version__ = 0.0

# Exportable API
__all__ = []

rank = MPI.COMM_WORLD.Get_rank()

size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()
library_version = MPI.Get_library_version()
version = MPI.Get_version()

if rank == 0:
    sys.stdout.write("[Rank 0] Hello, I'm special.\n")
    sys.stdout.write("\tsize = {}\n".format(size))
    sys.stdout.write("\tname = {}\n".format(name))
    sys.stdout.write("\tlibrary_version = {}\n".format(library_version))
    sys.stdout.write("\tversion = {}\n".format(version))

else:
    sys.stdout.write("[Rank {}] Hello.\n".format(rank))
