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

import math

import TAS_app
import TCS_configApp
# import TNS_node_tools as tools
import TCS_core
import TCS_interface
import TCS_utils


class step_info:
    def __init__(self, app: TAS_app.app):
        self.app = app
        self.name = app.name
        self.step_time = app._app_config.step_time
        self.step_on_start = app._app_config.step_on_boot
        self.step_on_shutdown = app._app_config.step_on_shutdown
        self.step_count = 1
        self.status = "RUNNING"


class node(TCS_core.core):
    def __init__(self, nodeName, testAll: bool = False) -> None:
        # super overrides the init function of the core class
        super().__init__()
        self.version = TCS_utils.version()

        self.name = nodeName
        self.description = "Node class for TWnode"
        self.interface.update_dir()

        # set up info
        self.testAll = testAll

        self.app_list: list[step_info] = []
        self.boot_list = []

        self.step_time = 1
        self.interface = TCS_interface.node_interface(self)
        # end
        self.interface.dlog(
            f"{self.name} v{self.version} : NODE-BASE INITIALIZED", logType="INFO")

    def add_app(self, app: TAS_app.app, app_parameters: TCS_configApp._app_config) -> None:
        """
        Adds an app to the Node
        """
        self.boot_list.append(app)
        _temp_app = app.TUAapp(app_parameters)
        _temp_app._settings()
        self.app_list.append(step_info(_temp_app))
        self.interface.log(
            f"{self.name} v{self.version} : APP ADDED", logType="INFO")

    def _start_base(self):
        self.calc_step_time()
        self.ProcessTable()
        for self.i in self.app_list:
            try:
                self.i.app._start()
            except:
                self.interface.log("app start failed: " + self.i.name, "ERROR")

    def _step_base(self):

        self.errorNum = 0
        self.errorList = []
        for self.i in self.app_list:
            if self.step_count == 1 and self.i.step_on_start == True:
                status = self._app_step(self.i)
                if status:
                    self.interface.log(
                        'START UP STEP SUCCESSFUL: ' + self.i.name, logType="STEP")
            elif self.step_count % self.i.step_count == 0:
                self._app_step(self.i)

        self.interface.log("COMPLETE | step error count = " + str(self.errorNum) +
                           " | step error list = " + str(self.errorList), logType="STEP")

    def _app_step(self, app_info: step_info):
        try:
            app_info.app.step()
            return True
        except Exception as e:
            self.errorNum += 1
            self.errorList.append(app_info.app.name)
            self.interface.log(
                "Error in app " + app_info.app.name + " Unable to process step : " + str(e), logType="STEP ERROR")
            try:
                app_info.app.interface.log(
                    "Error in app " + app_info.app.name + " Unable to process step : " + str(e), logType="STEP ERROR")
            except:
                pass
        return False

    def calc_step_time(self):
        """
        calculate the time for each step
        """
        if len(self.app_list) == 0:
            self.interface.log("No apps to calculate step time", logType="STEP")
            self.interface.log("NO APPS LOADED: EXIT CODE 2", "CRITICAL ERROR - EXIT")
            exit()
            return
        elif len(self.app_list) == 1:
            # self.app_list[0][2] = self.app_list[0][4] - self.app_list[0].step_on_start
            self.interface.dlog("Step time calculated for " +
                                self.app_list[0].name, logType="STEP")
            self.step_time = self.app_list[0].step_time
            return
        else:

            times = []
            for app in self.app_list:
                times.append(app.step_time)
            # find gcd of requested step times
            self.step_time = times[0]
            for i in range(1, len(times)):
                self.step_time = math.gcd(self.step_time, times[i])
            # assign step count to each app
            for app in self.app_list:
                step_count = app.step_time / self.step_time
                app.step_count = int(step_count)

        self.interface.dlog("Step Time = " + str(self.step_time))

    def ProcessTable(self):
        tabFormat = "|{:^16}|{:^10}|{:^10}|{:^12}|{:^12}|{:^15}|{:^16}|"
        self.interface.log(tabFormat.format('APP', 'APP NAME', "STEP TIME",
                                            'STEP ON BOOT', 'STEP ON END', 'STEP INTERVAL', "STATUS"))
        for info in self.app_list:
            self.interface.log(tabFormat.format(
                str(info.app.__module__), info.name, str(info.step_time), str(info.step_on_start),
                str(info.step_on_shutdown), str(info.step_count), info.status))


if __name__ == "__main__":
    pass
