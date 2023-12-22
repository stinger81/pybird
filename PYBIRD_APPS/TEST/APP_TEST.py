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

import random
import string
from datetime import datetime, timezone

import TAS_app
import TCS_configApp
import TCS_utils


class TUAapp(TAS_app.app):
    def __init__(self, parameters: TCS_configApp._app_config, test: bool = False):
        super().__init__("TEST", parameters, test)
        self.name = "TEST"
        self.version = TCS_utils.app_version()
        self.version.major = 0
        self.version.minor = 1
        self.version.patch = 0

        self.description = "TEST app"

    def myStart(self):
        """
        This should be used to set all variables that need to be initialized when the app starts
        """
        self.tweets_DB = self.data_pool.get_collection("Tweets")
        self.passcount = 0
        self.maxpass = 4

    def myStep(self):
        """
        override step
        """
        tweet = str(datetime.now(timezone.utc)) + "-TEST ID: "
        testID = ""
        for i in range(0, random.randrange(8, 64)):
            if random.randrange(0, 2) == 0:
                testID += str(random.randrange(0, 9))
            else:
                testID += random.choice(string.ascii_letters)

        tweet += testID
        # insert tweet into database
        self.tweets_DB.insert_one({"date": datetime.now(timezone.utc),
                                   "test_id": testID,
                                   "tweet": tweet,
                                   "length": len(tweet)})
        # log tweet length
        self.interface.log(str("Tweet Length " + str(len(tweet))), "INFO")
        # silently log a message to the database/local
        self.interface.log_db(tweet, "TWEET")
        self.tweet.post_tweet(tweet)

        self.passcount += 1
        if self.passcount >= self.maxpass:
            self.interface.log("MAX TEST PASSES REACHED: EXIT CODE 0", "Shutdown by exit")
            exit(0)


if __name__ == "__main__":
    app = TMSapp()
    app._run()
    app.step()
