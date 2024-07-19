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

import subprocess

import TAS_app_base
import TCS_configApp
import TCS_utils
import TCS_variables


class TUAapp(TAS_app_base.app):
    def __init__(self, parameters: TCS_configApp._app_config, test: bool = False):
        super().__init__(parameters.app_code, parameters, test)
        self.name = parameters.app_code
        self.version = TCS_utils.app_version()
        self.version.major = 1
        self.version.minor = 0
        self.version.patch = 0

        self.description = "System Monitor App"

        self.save_file = self._app_config.app_parameters["data_log_csv"]

    def myStart(self):
        """
        This should be used to set all variables that need to be initialized when the app starts
        """
        pass

    def myLoad(self):
        """
        This should be used to load all variables that need to be loaded between instances
        """
        pass

    def mySave(self):
        """
        This should be used to save all variables that need to be saved between instances
        """
        pass

    def myTimeRequest(self):
        """
        Used to send next step time to system
        :return:
        """
        return None

    def myStep(self):
        """
        override step
        """
        if TCS_variables.PLATFORM_UNIX_BASED and TCS_variables.PLATFORM_REMOTE_SERVER:
            self.interface.log("Commanding System Reboot in 60 Seconds", self.interface.SYSTEM_NOTICE)
            self.rebootSystem()
    def rebootSystem(self) -> None:
        # once the message system is implemented, this will be a message to the system
        # it will command all apps to stop and shutdown
        # once all apps are terminated it will do a reboot. for now we exit and let the destructors handle it
        subprocess.call(["shutdown", "-r", "-t", "60"])
        self.interface.log("Clean Exit From Pybird Exit(0)", self.interface.EXIT)
        exit(0)




if __name__ == "__main__":
    app = TMSapp()
    app._run()
    app.step()
