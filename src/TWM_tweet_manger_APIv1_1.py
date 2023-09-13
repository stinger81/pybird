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

import time

import tweepy

import TCS_utils
import TWM_key_manager

"DEPRECATED AS OF 0.8-DEV USE V2"


class Bot:
    def __init__(self, app, keys: TWM_key_manager.keys):
        self.version = TCS_utils.version()

        self._app = app

        self._bearer_token = keys.bearer_token
        self._consumer_key = keys.api_key
        self._consumer_secret = keys.api_secret
        self._access_token = keys.access_token
        self._access_secret = keys.access_token_secret

        self.post_allowed = False
        self.access_twitter = False
        # try:
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_secret)

        self.client = tweepy.API(auth)

        # print(self.client.verify_credentials()._json)
        self._client_id = self.client.verify_credentials().id

    def init_account(self):

        if len(self.client.user_timeline(count=1)) <= 0:
            self._app.interface.log("Sending Hello World", logType="TWEET")
            self._post_tweet("Hello World")
            time.sleep(5)

    def get_last_tweet(self):
        if self.access_twitter:
            # tweet = self.client.user_timeline(id = self._client_id, count = 1)[0]
            tweet = self.client.user_timeline(
                user_id=self._client_id, count=1)[0]
            return tweet
        else:
            self._app.interface.log("No access to twitter", logType="WARNING")
            return None

    def post_tweet(self, tweet):

        if self.get_last_tweet().text == tweet:
            self._app.interface.log(
                "Tweet already posted unable to post", logType="WARNING")
        else:
            self._post_tweet(tweet)

    def _post_tweet(self, tweet):

        if self.post_allowed:
            if self.validate_tweet(tweet):
                self.client.update_status(tweet)
                self._app.interface.log(tweet, logType="TWEET OUT")
        else:
            self._app.interface.log(
                "Posting not allowed", logType="WARNING")

    def get_tweet_post_time(self, tweet):
        return tweet.created_at

    def validate_tweet(self, tweet):
        valid = True

        if len(str(tweet)) > self._app._config.twitter.max_char:
            valid = False
            self._app.interface.log("(1/2) length tweet longer than 280 char", logType="TWEET ERROR")
            self._app.interface.log("(2/2) Attempted Tweet:" + str(tweet), logType="TWEET ERROR")

        return valid


if __name__ == '__main__':
    pass
