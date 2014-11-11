# -*- coding: utf8 -*-
# SDAPS - Scripts for data acquisition with paper based surveys
# Copyright(C) 2008, Christoph Simon <post@christoph-simon.eu>
# Copyright(C) 2008, Benjamin Berg <benjamin@sipsolutions.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

u"""
This modules contains a GTK+ user interface. With the help of this GUI it is
possible to manually correct the automatic recognition and do basic debugging.
"""

from sdaps import model
from sdaps import script

from sdaps.ugettext import ugettext, ungettext
_ = ugettext


parser = script.subparsers.add_parser("gui",
    help=_("Launch a gui. You can view and alter the (recognized) answers with it."),
    description=_("""This command launches a graphical user interface that can
    be used to correct answer. You need to run "recognize" before using it.
    """))

parser.add_argument('-f', '--filter',
    help=_("Filter to only show a partial dataset."))

@script.connect(parser)
@script.logfile
def gui(cmdline):
    survey = model.survey.Survey.load(cmdline['project'])
    import gui
    return gui.gui(survey, cmdline)


