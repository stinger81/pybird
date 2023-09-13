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
import TAS_app
import TCS_configApp
import TCS_utils


class TUAapp(TAS_app.app):
    def __init__(self, parameters: TCS_configApp._app_config, test: bool = False):
        super().__init__("APP_NAME", parameters, test)
        self.name = "APP_NAME"
        self.version = TCS_utils.app_version()
        self.version.major = 0
        self.version.minor = 0
        self.version.patch = 0

        self.description = "EXAMPLE APP"
        self.author = "XXXXXXXXXXXXXX"
        self.email = "XXXXXXXXXXXXXX"
        self.url = "XXXXXXXXXXXXXX"

    # DO NOT ADD ANY CODE TO INITIALIZE YOUR APP HERE!

    def mySettings(self):
        # ADD YOUR APP INITIALIZATION CODE HERE!
        pass

    def myStep(self):
        """
        override step
        """
        # code that should be executed on each step
        # use 'self.tweet.post_tweet(str())' to post a tweet
        pass


if __name__ == "__main__":
    app = TUAapp()
    app._run()
    app.step()
