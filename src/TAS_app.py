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

"""
Base class for apps

"""
import TAS_app_plugins
import TCS_config
import TCS_configApp
import TCS_core
import TCS_interface
import TCS_utils
import TCS_variables
import TDS_NVM
import TDS_database_atlas
import TWM_key_manager
import TWM_tweet_manger_APIv1_1
import TWM_tweet_manger_APIv2


class app(TCS_core.core):
    def __init__(self, name, parameters: TCS_configApp._app_config, test: bool = False):
        super().__init__()
        if name != parameters.app_code:
            self.interface.log(str(
                "App Code [" + parameters.app_code + "] does NOT match App Name [" + str(name) + "]"),
                logType="CRITICAL ERROR")
            raise (KeyError(str(
                "App Code [" + parameters.app_code + "] does NOT match App Name [" + str(name) + "]")))

        self.version = TCS_utils.version()

        # config set up
        self._app_config: TCS_configApp._app_config = parameters
        self.name: str = self._app_config.app_code
        self._config: TCS_config.TCS_config = TCS_config.TCS_config()

        # interface initial set up
        self.description: str = "TWapp"
        self.interface.update_dir()
        self.test: bool = test

        # is it an app
        self.isApp = True
        self.interface = TCS_interface.app_interface(self)
        # display test mode message 
        if test:
            self.interface.log("Started in test mode TEST MODE", logType="INFO")

        # get twitter keys
        self.key = TWM_key_manager.keys(self)

        self.tweet_enabled = self.key.load_keys()

        if self.tweet_enabled:
            self.interface.dlog("using api v2", "API VERSION")
            self.tweet = TWM_tweet_manger_APIv2.Bot(self, self.key)
            self.tweet.access_twitter = True
            self.tweet.post_allowed = True
        else:
            self.interface.log("Tweeting disabled", "ERROR")

        #  database initial set up
        if self._app_config.DB_dedicated_access:
            self._data_pool = TDS_database_atlas.mongodb_atlas(self, self._app_config.DB_dedicated_name)
            if self._data_pool.valid:
                self.data_pool = self._data_pool.db
            else:
                self.data_pool = None
                self.interface.log("Dedicated Data Pool Disabled", "ERROR")
                self._app_config.DB_dedicated_access = False
                self.interface.log("setting log to db to disabled", "ERROR")

        if self._app_config.DB_shared_access:
            self._shared_data_pool = TDS_database_atlas.mongodb_atlas(self, self._app_config.DB_shared_name)
            if self._shared_data_pool.valid:
                self.shared_data_pool = self._shared_data_pool.db
            else:
                self.shared_data_pool = None
                self.interface.log("Shared Data Pool Disabled", "ERROR")

        if self._app_config.DB_dedicated_access and self._app_config.log_to_DB:
            self.interface._add_collection(self.data_pool.get_collection(TCS_variables.ATLAS_LOG_COLLECTION))

        self.data_interface = TDS_NVM.data_interface(self.name)

        self.plugins = TAS_app_plugins.plugins()
        self.interface.dlog(
            f"{self.name} v{self.version} : APP-BASE INITIALIZED", logType="INFO")

    def use_twitter_v1_1(self):
        self.interface.dlog("using api v1.1", "API VERSION")
        if self.tweet_enabled:
            self.tweet = TWM_tweet_manger_APIv1_1.Bot(self, self.key)
            self.tweet.access_twitter = True
            self.tweet.post_allowed = True
            self.tweet.init_account()
        else:
            self.interface.log("Tweeting disabled", "ERROR")

    def _run_base(self):
        pass

    def _settings_base(self):
        pass

    def _step_base(self):
        pass
