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

import argparse
import logging
import sys

__version__ = 0.0

# Exportable API
__all__ = ['main', 'parse_args']


def parse_args(*args, **kwargs):
    """
    Parse the arguments received from STDIN.
    :param args: The string arguments to be parsed.
    :return params: The arguments parsed into parameters.
    :rtype: argparse.Namespace
    """
    # Constructing argument parser
    parser = argparse.ArgumentParser(description="A <بعض المرافق>.")

    parser.add_argument("positionals", type=int, nargs='?', default=8, help="A number of positionals.")
    mtxgrp = parser.add_mutually_exclusive_group()
    mtxgrp.add_argument("-x", "--letterx", type=str, default='x', help="The letter x.")
    mtxgrp.add_argument("-y", "--lettery", default=False, action='store_true', help="The letter y.")
    mtxgrp.add_argument("-z", "--letterz", type=int, default=3, help="The letter z.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Amount of output during runtime.")
    parser.add_argument("--version", action='version', version='cli %s' % __version__)

    # Process and return parameters
    return parser.parse_args(*args, **kwargs)


def main(params):
    """
    Execute the main method of the program.
    :param params: The parameters that will dictate the functionality of the program.
    :return: The final return code of the program.
    :rtype: int
    """

    # Set up logging
    if params.verbose == 1:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif params.verbose == 2:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    logging.debug(params)
    logging.info("مرحبا بالعالم.")


if __name__ == '__main__':
    sys.exit(main(parse_args()))
