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


import TCS_config
import TCS_configApp
import TCS_core
import TCS_interface
import TCS_utils
import TDS_NVM
import TDS_file


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
        self.save_key = self._app_config.save_key

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

        # NVM initial set up
        self.data_interface = TDS_NVM.NVM_dataInterface(self.name, save_key=self.save_key)
        self.file_interface = TDS_file.TDS_file(self.name, save_key=self.save_key)

        self.interface.dlog(
            f"{self.name} v{self.version} : APP-BASE INITIALIZED", logType="INFO")

    def _run_base(self):
        pass

    def _settings_base(self):
        pass

    def _step_base(self):
        pass

    def myLoad(self):
        # to be overridden in parent class
        pass

    def mySave(self):
        # to be overridden in parent class
        pass

    def preStep(self):
        """
        Pre step
        :return:
        """
        if self._app_config.load_before_each_step:
            self.myLoad()

    def postStep(self):
        """
        Post step
        :return:
        """
        if self._app_config.save_after_each_step:
            self.mySave()

    def myTimeRequest(self):
        # to be overridden in parent class
        pass
