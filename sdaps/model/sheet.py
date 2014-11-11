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

import buddy


class Sheet(buddy.Object):

    def __init__(self):
        self.survey = None
        self.data = dict()
        self.images = list()
        self.survey_id = None
        self.questionnaire_id = None
        self.global_id = None
        self.valid = 1
        self.quality = 1

    def add_image(self, image):
        self.images.append(image)
        image.sheet = self

    def get_page_image(self, page):
        # Simply return the image for the requested page.
        # Note: We return the first one we find; this means in the error case
        #       that a page exists twice, we return the first one.
        for image in self.images:
            if image.page_number == page and image.survey_id == self.survey.survey_id:
                return image
        return None

class Image(buddy.Object):

    def __init__(self):
        self.sheet = None
        self.filename = str()
        self.tiff_page = 0
        self.rotated = 0
        self.raw_matrix = None
        self.page_number = None
        self.survey_id = None
        self.global_id = None
        self.questionnaire_id = None

