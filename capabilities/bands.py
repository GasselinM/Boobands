# -*- coding: utf-8 -*-

# Copyright(C) 2018 Maxime Gasselin et Quentin Defenouillère
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


from datetime import datetime, date

from weboob.tools.compat import basestring, unicode

from .base import Capability, BaseObject, Field, StringField, UserError, NotLoaded
from .date import DateField

__all__ = ['Bandinfo', 'Bandsearch', 'BandNotFound', 'CapBands', 'Favorites', 'Suggestion']


class Bandinfo(BaseObject):
    """
    Information about one specific band.
    """
    name =             StringField('Name of band')
    genre =            StringField('Music genre of the band')
    year =             StringField('Year of creation')
    country =          StringField('Country of origin')
    description =      StringField('Description of the band')

    def __init__(self, year=None, country=None, genre=None, description=None, url=None):
        super(Bandinfo, self).__init__(id, url)
        self.genre = genre
        self.year = year
        self.description = description
        self.country = country


class Bandsearch(BaseObject):
    """
    Bands search.
    """
    name =                  StringField('Name of band')
    short_description =     StringField('Short description of the band')

    def __init__(self, id='', name=None, short_description=None, url=None):
        super(Bandsearch, self).__init__(id, url)
        self.name = name
        self.short_description = short_description


class Favorites(BaseObject):
    """
    Your favorite bands.
    """
    name =                  StringField('Name of favorite band')
    band_url =              StringField('URL of the favorite band')
    short_description =     StringField('Short description of the favorite band')

    def __init__(self, id='', name=None, band_url=None, short_description=None):
        super(Favorites, self).__init__(id, band_url)
        self.name = name
        self.band_url = band_url
        self.short_description = short_description

class Suggestion(BaseObject):
    """
    Bands search.
    """
    name =                  StringField('Suggested band')
    band_url =              StringField('URL of the favorite band')


    def __init__(self, id='', name=None, band_url=None):
        super(Suggestion, self).__init__(id, band_url)
        self.name = name
        self.band_url = band_url


class BandNotFound(UserError):
    """
    Raised when a city is not found.
    """


class CapBands(Capability):
    """
    Capability for weather websites.
    """

    def iter_band_search(self, pattern):
        """
        Look for a band.

        :param pattern: pattern to search
        :type pattern: str
        :rtype: iter[:class:`Bandsearch`]
        """
        raise NotImplementedError()

    def get_info(self, band_id):
        """
        Get band info.

        :param band_id: ID of the band
        :rtype: :class:`Bandinfo`
        """
        raise NotImplementedError()

    def get_favorite(self):
        """
        Get my favorite bands.

        :rtype: iter[:class:`Favorites`]
        """
        raise NotImplementedError()

    def suggestion(self):
        """
        Get my favorite bands.

        :rtype: iter[:class:`Favorites`]
        """
        raise NotImplementedError()

