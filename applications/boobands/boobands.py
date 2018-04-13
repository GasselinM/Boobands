# -*- coding: utf-8 -*-

# Copyright(C) 2018  Maxime Gasselin et Quentin Defenouillère
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


from weboob.capabilities.base import empty
from weboob.capabilities.bands import CapBands
from weboob.tools.application.repl import ReplApplication, defaultcount
from weboob.tools.application.formatters.iformatter import IFormatter, PrettyFormatter


__all__ = ['Boobands']


class BandInfoFormatter(PrettyFormatter):
    MANDATORY_FIELDS = ('id', 'name', 'genre', 'year', 'country', 'description')
    def format_obj(self, obj, alias):
        result = u'\n%s%s%s\n' % (self.BOLD, obj.name, self.NC)
        if not empty(obj.genre):
            result += 'Genre: %s\n' % obj.genre
        if not empty(obj.country):
            result += 'Country: %s\n' % obj.country
        if not empty(obj.year):
            result += 'Formed in: %s\n' % obj.year
        if not empty(obj.description):
            result += '%sDescription:%s\n' % (self.BOLD, self.NC)
            result += '%s\n' % obj.description
        return result.strip()


class BandListFormatter(PrettyFormatter):
    MANDATORY_FIELDS = ('id', 'name', 'short_description')

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        result = u''
        if not empty(obj.short_description):
            result += '%s\n' % obj.short_description
        return result.strip()


class FavoritesFormatter(PrettyFormatter):
    MANDATORY_FIELDS = ('id', 'name', 'band_url', 'short_description')

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        result = u''
        if not empty(obj.id):
            result += '%s\n' % obj.id
        if not empty(obj.short_description):
            result += '\t%s\n' % obj.short_description
        return result.strip()

class SuggestFormatter(PrettyFormatter):
    MANDATORY_FIELDS = ('id', 'name', 'band_url')

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        result = u''
        if not empty(obj.band_url):
            result += '%s\n' % obj.band_url
        return result.strip()


class Boobands(ReplApplication):
    APPNAME = 'boobands'
    VERSION = '1.4'
    COPYRIGHT = 'Copyright(C) 2018-YEAR QDef et MaxG'
    DESCRIPTION = "Console application allowing to display music bands and offer music suggestions."
    SHORT_DESCRIPTION = "Display bands and suggestions"
    CAPS = CapBands
    DEFAULT_FORMATTER = 'table'
    EXTRA_FORMATTERS = {'band_search':    BandListFormatter,
                        'band_info':   BandInfoFormatter,
                        'get_favorites' : FavoritesFormatter,
                        'suggestion': SuggestFormatter,
                       }

    COMMANDS_FORMATTERS = {'search':  'band_search',
                           'info':   'band_info',
                           'favorites' : 'get_favorites',
                           'suggestion' : 'suggestion'
                          }


    def main(self, argv):
        self.load_config()
        return ReplApplication.main(self, argv)

    @defaultcount(20)
    def do_search(self, pattern):
        """
        band PATTERN
        Search bands.
        """
        self.change_path(['search'])
        self.start_format()
        for band in self.do('iter_band_search', pattern, caps=CapBands):
            self.cached_format(band)

    def complete_info(self, text, line, *ignored):
        args = line.split(' ')
        if len(args) == 1:
            return self._complete_object()

    def do_info(self, line):
        """
        info BAND_ID

        Get detailed info for specified band. Use the 'search' command to find bands.
        """
        band, = self.parse_command_args(line, 1, 1)
        _id, backend_name = self.parse_id(band)

        self.change_path(['info'])
        self.start_format()
        for info in self.do('get_info', _id, backends=backend_name, caps=CapBands):
            if info:
                self.format(info)

    #def complete_favorite(self, text, line, *ignored):
        #args = line.split(' ')
        #if len(args) == 1:
            #return self._complete_object()

    @defaultcount(40)
    def do_favorites(self, *ignored):
        """
        favorites

        Displays your favorite bands.
        """
        self.change_path(['favorite'])
        self.start_format()
        for favorite in self.do('get_favorites', caps=CapBands):
            self.cached_format(favorite)
    @defaultcount(500)
    def do_suggestion(self, *ignored):
        """
        suggestion

        Displays suggestion bands.
        """
        self.change_path(['suggestion'])
        self.start_format()
        for suggestion in self.do('suggestion', caps=CapBands):
            self.cached_format(suggestion)
