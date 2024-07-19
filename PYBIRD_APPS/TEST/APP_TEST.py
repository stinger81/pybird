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

import datetime
import random
import string

import TAS_app
import TCS_configApp
import TCS_utils


class TUAapp(TAS_app.app):
    def __init__(self, parameters: TCS_configApp._app_config, test: bool = False):
        super().__init__("TEST", parameters, test)
        self.name = "TEST"
        self.version = TCS_utils.app_version()
        self.version.major = 1
        self.version.minor = 0
        self.version.patch = 0

        self.description = "TEST app"



    def myStart(self):
        """
        This should be used to set all variables that need to be initialized when the app starts
        """

        self.tweet = self.plugins.SocialMedia.Twitter(self)
        self.mongo = self.plugins.DataBase.MongoDB(self)

        self.my_db = self.mongo.connect_to_database("TEST_DB")
        self.tweets_DB = self.my_db.get_collection("Tweets")
        self.passcount = 0
        self.maxpass = 3
        self.test_str = "This is a test string"
        self.last_step = datetime.datetime.utcnow()



    def myLoad(self):
        """
        This should be used to load all variables that need to be loaded between instances
        """
        self.test_str = self.data_interface.load("test")

    def mySave(self):
        """
        This should be used to save all variables that need to be saved between instances
        """
        self.test_str = "This is a test string" + str(random.randrange(0, 100))
        self.data_interface.save("test", self.test_str)

    def myTimeRequest(self):
        """
        Used to send next step time to system
        :return:
        """
        print("requesting time")
        return self.last_step + datetime.timedelta(seconds=10)

    def myStep(self):
        """
        override step
        """
        # my = 1 / 0
        self.last_step = datetime.datetime.utcnow()
        tweet = str(datetime.datetime.utcnow()) + "-TEST ID: "
        testID = ""
        for i in range(0, random.randrange(8, 64)):
            if random.randrange(0, 2) == 0:
                testID += str(random.randrange(0, 9))
            else:
                testID += random.choice(string.ascii_letters)

        tweet += testID
        # insert tweet into database
        self.tweets_DB.insert_one({"date": datetime.datetime.utcnow(),
                                   "test_id": testID,
                                   "tweet": tweet,
                                   "length": len(tweet)})
        # log tweet length
        self.interface.log(str("Tweet Length " + str(len(tweet))), "INFO")
        # silently log a message to the database/local
        if self._app_config.app_parameters["post"]:
            self.tweet.post(tweet)

        self.data_interface.save("test", tweet)

        self.passcount += 1
        if self.passcount >= self.maxpass:
            self.interface.log("MAX TEST PASSES REACHED: EXIT CODE 0", "Shutdown by exit")
            exit(0)


if __name__ == "__main__":
    app = TMSapp()
    app._run()
    app.step()
