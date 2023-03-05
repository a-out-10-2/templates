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
from enum import Enum
import logging
import sys

__version__ = 0.0

# Exportable API
__all__ = ['main', 'parse_args']


def parse_args(*args, **kwargs):
	"""Parse the arguments received from STDIN.
	param args: The string arguments to be parsed.
	return params: The arguments parsed into parameters.
	rtype: argparse.Namespace or RC
	"""

	class _ArgumentParser(argparse.ArgumentParser):
		""" Supress exit and raise exceptions on syntax errors"""
		FLAG_HELP = "--help"

		def __init__(self, description):
			super().__init__(description=description, exit_on_error=False)

		def exit(self, status=0, message=None):
			if status:
				raise argparse.ArgumentError(argument=None, message=f"(status: {status}, message: '{message}'")

		def error(self, message):
			raise argparse.ArgumentError(argument=None, message=message)

	# Constructing argument parser
	parser = _ArgumentParser(description="* null *")
	parser.add_argument("positionals", type=str, nargs='+', help="A number of positional paths.")
	mutux = parser.add_mutually_exclusive_group()
	mutux.required = True  # Require a mutux option
	mutux.add_argument("-x", "--letterx", type=str, default='x', help="The letter x.")
	mutux.add_argument("-y", "--lettery", default=False, action='store_true', help="The letter y.")
	mutux.add_argument("-z", "--letterz", type=int, default=3, help="The letter z.")
	parser.add_argument("-hh", "--help-rc", default=False, action='store_true', help="Describe return codes.")
	parser.add_argument("-v", "--verbose", action="count", default=0, help="Amount of output during runtime.")
	parser.add_argument("--version", action='version', version='cli %s' % __version__)

	# Process and return parameters
	parsed_params = RC.SYNTAX_ERR
	try:
		parsed_params = parser.parse_args(*args, **kwargs)
	except argparse.ArgumentError as ae:
		if parser.FLAG_HELP not in list(*args):
			print(f"ArgumentError: {ae} (args: {list(*args)})", file=sys.stderr)

	return parsed_params


class RC(Enum):
	"""Possible return codes of CLI application."""
	PASS = 0, "Application exited nominally."
	SYNTAX_ERR = 1, "Application exited from incorrect syntax."


def main(params):
	"""Execute the main method of the program.
	:param params: The parameters that will dictate the functionality of the program.
	:return: The final return code of the program.
	:rtype: RC
	"""
	# Set up logging
	if params.verbose == 1:
		logging.basicConfig(format='%(message)s', level=logging.INFO)
	elif params.verbose == 2:
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)

	logging.debug("params: {params}")
	logging.info("مرحبا بالعالم.")

	logging.info(f"Just hangin', chompin' on positionals: {params.positionals}")


if __name__ == '__main__':
	sys.exit((
		lambda parsed_args: parsed_args if isinstance(parsed_args, RC) else main(parsed_args))(parse_args(sys.argv[1:]))
	)
