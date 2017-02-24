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
import threading

__version__ = 0.0

# Exportable API
__all__ = []

NTHREADS = 8


class ThreadClassTemplate(threading.Thread):

    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id

    def run(self):
        print("[Thread {}] Hello.".format(self.thread_id))

if __name__ == '__main__':

    # Spawn threads
    threads = [ThreadClassTemplate(i) for i in range(NTHREADS)]
    [thr.start() for thr in threads]
    [thr.join() for thr in threads]
