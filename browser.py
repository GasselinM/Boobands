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
from weboob.browser import URL, LoginBrowser, need_login
from .pages import BandPage, SearchBandsPage, LoginPage, FavoritesPage, SuggestionPage
import operator

__all__ = ['MetalarchivesBrowser']

class MetalarchivesBrowser(LoginBrowser):
    """Browsing the Metal Archives website """

    BASEURL = 'https://www.metal-archives.com/'
    login = URL('authentication/login', LoginPage)
    bands = URL('search/ajax-band-search/\?field=name&query=(?P<pattern>.*)', SearchBandsPage)
    band = URL('bands/(?P<band_id>.*)',  BandPage)
    favorites = URL('bookmark/ajax-list/type/band\?sEcho=1', FavoritesPage)
    suggest = URL('band/ajax-recommendations/id/(?P<pattern>.*)\?showMoreSimilar=1', SuggestionPage)

    def iter_band_search(self, pattern):
        return self.bands.go(pattern=pattern).iter_bands()

    def get_info(self, id):
        return self.band.go(band_id=id).get_info()

    @need_login
    def get_favorites(self):
        return self.favorites.go().iter_favorites()

    def do_login(self):
        d = {'loginUsername': self.username,
                'loginPassword': self.password}
        self.login.go(data=d)

    @need_login
    def suggestion(self, liste):
        """ suggestion tool does :
        - get all the id of all favorite bands
        - connect all suggestion pages from favorite bands
        - create dictionnary that counts all groups (avoid duplicate and add scores)
        - delete a group if this group is in the favorite
        - return a suggestion list based on the max score"""
        band = list(liste)
        suggestions=[]

        for ids in band:
            suggestions+= self.suggest.go(pattern=ids).iter_suggestion()
        dicbands= {}

        for group in suggestions:
            present=False
            for url in band:
                if url in group.band_url:
                    present=True
            if present == True:
                pass
            elif not group.band_url in dicbands:
                dicbands[group.band_url]=[1,group]
            else:
                dicbands[group.band_url][0] = dicbands[group.band_url][0] +1

        for _ in range(10):
            a= max(dicbands.items(), key=operator.itemgetter(1))[0]
            res = dicbands[a][1]
            dicbands.pop(a)
            yield res
