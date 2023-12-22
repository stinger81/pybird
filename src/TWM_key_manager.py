# /bin/python3
# ##########################################################################
#
#   Copyright (C) 2022-2024 Michael Dompke (https://github.com/stinger81)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Michael Dompke (https://github.com/stinger81)
#   michael@dompke.dev
#
# ##########################################################################

import tweepy

import TAS_app
import TCS_utils
import TKS_keychain

"""
Program to handle twitter keys.
"""


class keys:
    def __init__(self, app):
        self.version = TCS_utils.version()

        self._app: TAS_app.app = app

        self.keys = None

        self.client = None

        self.api_key = None
        self.api_secret = None
        self.bearer_token = None
        self.access_token = None
        self.access_token_secret = None
        self.client_id = None
        self.client_secret = None

    def load_keys(self):

        try:
            key_loader = TKS_keychain.keychain()
            self.keys = key_loader.load_twitter_keys(self._app.name)
            # self._load_keys()
            try:
                self._app.interface.dlog("Loading Keys")
                keys = self.keys.strip().split(",")
                self.api_key = keys[0]
                self.api_secret = keys[1]
                self.bearer_token = keys[2]
                self.access_token = keys[3]
                self.access_token_secret = keys[4]
                self.client_id = keys[5]
                self.client_secret = keys[6]

                self._app.interface.dlog("Validating Keys")

                auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
                auth.set_access_token(self.access_token, self.access_token_secret)

                self.client = tweepy.API(auth)
                self._client_id = self.client.verify_credentials().id
            except Exception as e:
                self._app.interface.log("Invalid Keys")
                e_mod = str(e).split("\n")
                for i in e_mod:
                    self._app.interface.log(i)
                return False
            return True


        except Exception as e:
            self._app.interface.log("Unable to load keys", logType="ERROR")
            e_mod = str(e).split("\n")
            for i in e_mod:
                self._app.interface.log(i)
            return False
