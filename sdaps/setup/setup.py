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

import os
import shutil

from sdaps import utils
from sdaps import model
from sdaps import log

from sdaps.ugettext import ugettext, ungettext
_ = ugettext

import buddies
import boxesparser
import qobjectsparser
import additionalparser
import metaparser
from pdftools import pdffile


def setup(survey, cmdline):

    if os.access(survey.path(), os.F_OK):
        log.error(_('The survey directory already exists.'))
        return 1

    questionnaire_odt = cmdline['questionnaire.odt']
    questionnaire_pdf = cmdline['questionnaire.pdf']
    additionalqobjects = cmdline['additional_questions']

    mimetype = utils.mimetype(questionnaire_odt)
    if mimetype != 'application/vnd.oasis.opendocument.text' and mimetype != '':
        log.error(_('Unknown file type (%s). questionnaire_odt should be application/vnd.oasis.opendocument.text.') % mimetype)
        return 1

    mimetype = utils.mimetype(questionnaire_pdf)
    if mimetype != 'application/pdf' and mimetype != '':
        log.error(_('Unknown file type (%s). questionnaire_pdf should be application/pdf.') % mimetype)
        return 1

    if additionalqobjects is not None:
        mimetype = utils.mimetype(additionalqobjects)
        if mimetype != 'text/plain' and mimetype != '':
            log.error(_('Unknown file type (%s). additionalqobjects should be text/plain.') % mimetype)
            return 1

    # Add the new questionnaire
    survey.add_questionnaire(model.questionnaire.Questionnaire())

    # Parse the box objects into a cache
    boxes, page_count = boxesparser.parse(questionnaire_pdf)
    survey.questionnaire.page_count = page_count

    # Get the papersize
    doc = pdffile.PDFDocument(questionnaire_pdf)
    page = doc.read_page(1)
    survey.defs.paper_width = abs(page.MediaBox[0] - page.MediaBox[2]) / 72.0 * 25.4
    survey.defs.paper_height = abs(page.MediaBox[1] - page.MediaBox[3]) / 72.0 * 25.4
    survey.defs.print_questionnaire_id = cmdline['print_questionnaire_id']
    survey.defs.print_survey_id = cmdline['print_survey_id']

    survey.defs.style = cmdline['style']
    # Force simplex if page count is one.
    survey.defs.duplex = False if page_count == 1 else cmdline['duplex']

    survey.global_id = cmdline['global_id']

    # Parse qobjects
    try:
        qobjectsparser.parse(survey, questionnaire_odt, boxes)
    except:
        log.error(_("Caught an Exception while parsing the ODT file. The current state is:"))
        print unicode(survey.questionnaire)
        print "------------------------------------"

        raise

    # Parse additionalqobjects
    if additionalqobjects:
        additionalparser.parse(survey, additionalqobjects)

    # Parse Metadata
    metaparser.parse(survey, questionnaire_odt)

    # Last but not least calculate the survey id
    survey.calculate_survey_id()

    if not survey.check_settings():
        log.error(_("Some combination of options and project properties do not work. Aborted Setup."))
        return 1

    # Print the result
    print survey.title

    for item in survey.info.items():
        print u'%s: %s' % item

    print unicode(survey.questionnaire)

    # Create the survey
    os.mkdir(survey.path())

    log.logfile.open(survey.path('log'))

    shutil.copy(questionnaire_odt, survey.path('questionnaire.odt'))
    shutil.copy(questionnaire_pdf, survey.path('questionnaire.pdf'))

    survey.save()
    log.logfile.close()

