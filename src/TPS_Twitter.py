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
import sys

import TCS_variables
import TWM_key_manager
import TWM_tweet_manger_APIv2


class Twitter:
    def __init__(self, app):
        self._app = app
        if self._app._app_config.plugin_twitter_enabled:
            self._key = TWM_key_manager.keys(self._app)
            self._tweet_enabled = self._key.load_keys()
        else:
            self._tweet_enabled = False

        if self._tweet_enabled:
            try:
                self._app.interface.dlog("using api v2", "API VERSION")
                self._tweet = TWM_tweet_manger_APIv2.Bot(self._app, self._key)
                self._tweet.access_twitter = True
                self._tweet.post_allowed = True
                self.client = self._tweet.client
            except Exception as e:
                self._tweet_enabled = False
                self._app.interface.log("Tweeting disabled", "ERROR")
                self._app.interface.log("Unable to validate keys/establish a connection", "ERROR")
                self._app.interface.log(e, "ERROR")
                if TCS_variables.SYS_ARG.RAISE[0] in sys.argv:
                    raise e

        else:
            self._app.interface.log("Tweeting disabled", "ERROR")

    def post(self, message) -> bool:
        if self._tweet_enabled:
            self._tweet.post_tweet(message)
            return True
        else:
            self._app.interface.log("Tweeting disabled: Unable to post Tweet", "ERROR")
            return False

    def validate(self, message) -> bool:
        return self._tweet.validate_tweet(message)
