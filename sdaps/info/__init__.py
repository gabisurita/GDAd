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

from sdaps import model
from sdaps import script
from sdaps import log

from sdaps.ugettext import ugettext, ungettext
_ = ugettext


parser = script.subparsers.add_parser("info",
    help=_("Display and modify metadata of project."),
    description=_("""This command lets you modify the metadata of the SDAPS
    project. You can modify, add and remove arbitrary keys that will be printed
    on the report. The only key that always exist is "title".
    If no key is given then a list of defined keys is printed."""))

parser.add_argument('key',
    nargs="?",
    help=_("The key to display or modify."))

parser.add_argument('-s', '--set',
    metavar="VALUE",
    help=_("Set the given key to this value."))

parser.add_argument('-d', '--delete',
    action="store_true",
    help=_("Delete the key and value pair."))


@script.connect(parser)
@script.logfile
def info(cmdline):
    survey = model.survey.Survey.load(cmdline['project'])

    if cmdline['key']:
        key = cmdline['key'].decode('utf-8').strip()
        if cmdline['set']:
            value = cmdline['set'].decode('utf-8').strip()
            if key == "title":
                survey.title = value
            else:
                survey.info[key] = value
        elif cmdline['delete']:
            del survey.info[key]
        else:
            if key == "title":
                print survey.title
            else:
                print survey.info[key]
    else:
        log.interactive(_(u'Existing fields:\n'))
        print "title"
        for key in survey.info.keys():
            print key

    survey.save()


