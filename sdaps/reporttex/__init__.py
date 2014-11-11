# -*- coding: utf8 -*-
# SDAPS - Scripts for data acquisition with paper based surveys
# Copyright(C) 2008, Christoph Simon <post@christoph-simon.eu>
# Copyright(C) 2008, 2011, Benjamin Berg <benjamin@sipsolutions.net>
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
This modules contains the functionality to create reports using LaTeX.
"""

from sdaps import model
from sdaps import script

from sdaps.ugettext import ugettext, ungettext
_ = ugettext

parser = script.subparsers.add_parser("report_tex",
    help=_("Create a PDF report using LaTeX."),
    description=_("""This command creates a PDF report using LaTeX that
    contains statistics and freeform fields."""))
parser.add_argument('-o', '--output',
    help=_("Filename to store the data to (default: report_%%i.pdf)"))

parser.add_argument('-f', '--filter',
    help=_("Filter to only export a partial dataset."))

@script.connect(parser)
@script.logfile
def report_tex(cmdline):
    survey = model.survey.Survey.load(cmdline['project'])
    import report
    return report.report(survey, cmdline['output'], cmdline['filter'])


