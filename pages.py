# -*- coding: utf-8 -*-

# Copyright(C) 2018      Maxime Gasselin et Quentin Defenouillère
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

from __future__ import unicode_literals
from weboob.browser.pages import JsonPage, HTMLPage, Page, RawPage, AbstractPage
from datetime import date
from weboob.browser.elements import ItemElement, ListElement, DictElement, method
from weboob.browser.filters.standard import Regexp, CleanText, Format, Env, CleanDecimal, Eval
from weboob.browser.filters.json import Dict
from weboob.capabilities.bands import Bandinfo, Bandsearch, Favorites, Suggestion # Album
from weboob.tools.json import json
from weboob.capabilities.base import NotAvailable

__all__ = ['SearchBandsPage', 'BandPage', 'FavoritesPage']

class SearchBandsPage(JsonPage):
    @method
    class iter_bands(DictElement):
        item_xpath = 'aaData'
        ignore_duplicate = True

        class item(ItemElement):
            klass = Bandsearch
            obj_id=Regexp(Dict('0'), 'bands/([^"]+)')
            obj_name=Regexp(Dict('0'), '>([^<]+)')
            obj_short_description = Format('Genre: %s - Country: %s', Dict('1'), Dict('2'))


class BandPage(HTMLPage):
    @method
    class get_info(ItemElement):
        klass = Bandinfo
        obj_id = Env('band_id')
        obj_name = CleanText('//h1[@class="band_name"]/a/text()')
        obj_genre = CleanText('//dl[@class="float_right"]/dd[1]/text()')
        obj_country = CleanText('//dl[@class="float_left"]/dd[1]/a/text()')
        obj_year = CleanText('//dl[@class="float_left"]/dd[4]/text()')
        obj_description = CleanText('//div[@class="band_comment clear"]/text()')


class FavoritesPage(JsonPage):
    """
    Display the list of your favorite bands.
    """
    @method
    class iter_favorites(DictElement):
        item_xpath = 'aaData'
        ignore_duplicate = True

        class item(ItemElement):
            klass = Favorites
            #obj_id=Regexp(Dict('0'), 'bands/([^"]+)')
            obj_id = Regexp(Dict('0'), 'href=\"([^"]+)')
            obj_name=Regexp(Dict('0'), '>([^<]+)')            
            obj_band_url =  Regexp(Dict('0'), '/([0-9]+)\\"')
            obj_short_description = Format('Genre: %s - Country: %s', Dict('2'), Dict('1'))


class LoginPage(HTMLPage):
    """
    Login to your Metal Archives account.
    """
    @property
    def logged(self):
        return self.doc['Success']

class SuggestionPage(HTMLPage):
    """
    Displays band suggestions depending on your favorite bands.
    """
    @method
    class iter_suggestion(ListElement):
        item_xpath = '//tbody/tr[position()<last()]'
        class item(ItemElement):
            klass = Suggestion
            #obj_id = CleanText('./td[1]/a/@href')
            obj_name = CleanText('./td[2]/a/text()')
            obj_band_url = CleanText('./td[2]/a/@href')
