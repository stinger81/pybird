# /bin/python3
# ##########################################################################
#
#   Copyright (C) 2022-2023 Michael Dompke (https://github.com/stinger81)
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

    def load_keys(self):

        try:
            key_loader = TKS_keychain.keychain()
            self.keys = key_loader.load_twitter_keys(self._app.name)
            self._load_keys()
            try:
                self._app.interface.dlog("Validating Keys")
                self._bearer_token = self.bearer_token
                self._consumer_key = self.api_key
                self._consumer_secret = self.api_secret
                self._access_token = self.access_token
                self._access_secret = self.access_token_secret

                auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
                auth.set_access_token(self._access_token, self._access_secret)

                self.client = tweepy.API(auth)

                # print(self.client.verify_credentials()._json)
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

    def _load_keys(self):

        try:
            self.api_key = self.keys['api_key']
        except:
            self._app.interface.log("No api_key found", logType="WARNING")
            self.api_key = None
        try:
            self.api_secret = self.keys['api_secret']
        except:
            self._app.interface.log("No api_secret found", logType="WARNING")
            self.api_secret = None
        try:
            self.bearer_token = self.keys['bearer_token']
        except:
            self._app.interface.log("No bearer_token found", logType="WARNING")
            self.bearer_token = None
        try:
            self.access_token = self.keys['access_token']
        except:
            self._app.interface.log("No access_token found", logType="WARNING")
            self.access_token = None
        try:
            self.access_token_secret = self.keys['access_token_secret']
        except:
            self._app.interface.log(
                "No access_token_secret found", logType="WARNING")
            self.access_token_secret = None
        try:
            self.client_id = self.keys['client_id']
        except:
            self._app.interface.log("No client_id found", logType="WARNING")
            self.client_id = None
        try:
            self.client_secret = self.keys['client_secret']
        except:
            self._app.interface.log("No client_secret found", logType="WARNING")
            self.client_secret = None
        return True
