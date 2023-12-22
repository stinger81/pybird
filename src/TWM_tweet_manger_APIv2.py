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

import TCS_utils
import TWM_key_manager


class Bot:
    def __init__(self, app, keys: TWM_key_manager.keys):
        self.version = TCS_utils.version()

        self._app = app

        self.keys = keys

        self.post_allowed = False
        self.access_twitter = False

        self.client = tweepy.Client(bearer_token=self.keys.bearer_token,
                                    consumer_key=self.keys.api_key,
                                    consumer_secret=self.keys.api_secret,
                                    access_token=self.keys.access_token,
                                    access_token_secret=self.keys.access_token_secret)

    def post_tweet(self, tweet):
        self._post_tweet(tweet)

    def _post_tweet(self, tweet):

        if self.post_allowed:
            if self.validate_tweet(tweet):
                self.client.create_tweet(text=tweet)
                self._app.interface.log(tweet, logType="TWEET OUT")
        else:
            self._app.interface.log(
                "Posting not allowed", logType="WARNING")

    def validate_tweet(self, tweet):
        valid = True

        if len(str(tweet)) > self._app._config.twitter.max_char:
            valid = False
            self._app.interface.log("(1/2) length tweet longer than 280 char", logType="TWEET ERROR")
            self._app.interface.log("(2/2) Attempted Tweet:" + str(tweet), logType="TWEET ERROR")

        return valid


if __name__ == '__main__':
    pass
