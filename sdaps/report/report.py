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

from reportlab import platypus

from sdaps import model

from sdaps import clifilter
from sdaps import template
from sdaps import matrix

from sdaps.ugettext import ugettext, ungettext
_ = ugettext

import buddies


def report(survey, filter, filename=None, small=0):
    assert isinstance(survey, model.survey.Survey)

    # compile clifilter
    filter = clifilter.clifilter(survey, filter)

    # First: calculate buddies

    # init buddies
    survey.questionnaire.calculate.init()

    # iterate over sheets
    survey.iterate(
        survey.questionnaire.calculate.read,
        lambda: survey.sheet.valid and filter()
    )

    # do calculations
    survey.questionnaire.calculate.calculate()

    # Second: report buddies

    # init buddies
    survey.questionnaire.report.init(small)

    # iterate over sheets
    survey.iterate(
        survey.questionnaire.report.report,
        lambda: survey.sheet.valid and filter()
    )

    # create story
    story = template.story_title(
        survey,
        {
            _(u'Turned in Questionnaires'): survey.questionnaire.calculate.count,
        }
    )
    story.extend(survey.questionnaire.report.story())

    # create report(out of story)
    if filename is None:
        filename = survey.new_path('report_%i.pdf')
    subject = []
    for key, value in survey.info.iteritems():
        subject.append(u'%(key)s: %(value)s' % {'key': key, 'value': value})
    subject = u'\n'.join(subject)

    doc = template.DocTemplate(
        filename,
        _(u'sdaps report'),
        {
            'title': survey.title,
            'subject': subject,
        }
    )
    doc.build(story)


def stats(survey, filter, filename=None, small=0):
    if filename is None:
        filename = survey.new_path('report_%i.pdf')

    # do a report
    report(survey, filter, filename=filename, small=small)

    # save reference (to highlight large differences)
    survey.questionnaire.calculate.reference()

    # do a report for every filter
    for i, subfilter in enumerate(survey.questionnaire.report.filters()):
        if filter is None:
            filt = subfilter
        else:
            filt = "(%s) and (%s)" % (filter, subfilter)
        report(
            survey, filt,
            filename='%s_%i %s.pdf' % (filename.split('.')[0], i, subfilter),
            small=small)

