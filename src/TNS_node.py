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
import sys

import TAS_app
import TCS_configApp
# import TNS_node_tools as tools
import TCS_core
import TCS_interface
import TCS_timing_manager
import TCS_utils
import TCS_variables


class step_info:
    def __init__(self, app: TAS_app.app):
        self.app = app
        self.name = app.name
        self.timing_manager = TCS_timing_manager.TimingManager(
            app.name, app._app_config)
        # self.step_time = app._app_config.step_time
        # self.step_on_start = app._app_config.step_on_boot
        # self.step_on_shutdown = app._app_config.step_on_shutdown
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
            f"{self.name} v{self.version} : APP ADDED {_temp_app.name}", logType="INFO")

    def _start_base(self):
        # self.calc_step_time()
        # self.ProcessTable()
        for app in self.app_list:
            try:
                app.timing_manager.set_next_time()
                app.app._start()
            except Exception as e:
                self.interface.log(f"Error: {e}", logType="ERROR")
                if TCS_variables.SYS_ARG.RAISE[0] in sys.argv:
                    raise e

    def _step_base(self):

        self.errorNum = 0
        self.errorList = []
        apps_ran = []

        for app in self.app_list:
            next_time = app.timing_manager.get_cur_time()
            if next_time == "request":
                next_time = app.app.myTimeRequest()
            elif next_time == "never":
                continue

            if next_time.timestamp() <= datetime.datetime.utcnow().timestamp():

                self._app_step(app)
                app.timing_manager.set_next_time()
                if app.step_count == 1:
                    self.interface.dlog(
                        'FIRST STEP SUCCESSFUL: ' + app.name, logType="STEP")
                app.step_count += 1
                apps_ran.append(app.name)

            # if self.step_count == 1 and self.i.step_on_start == True:
            #     status = self._app_step(self.i)
            #     if status:
            #         self.interface.log(
            #             'START UP STEP SUCCESSFUL: ' + self.i.name, logType="STEP")
            # elif self.step_count % self.i.step_count == 0:
            #     self._app_step(self.i)
        if len(apps_ran) == 0:
            self.interface.dlog("NO APPS RAN", logType="STEP")
        else:

            self.interface.log("COMPLETE | step error count = " + str(self.errorNum) +
                                " | step apps ran = " + str(apps_ran) + " | step error list = " + str(self.errorList),
                                logType="STEP")

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
            if TCS_variables.SYS_ARG.RAISE[0] in sys.argv:
                raise e
        return False




if __name__ == "__main__":
    pass
