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

import importlib
import os
import sys

import TCS_configApp
import TCS_utils
import TCS_variables
import TNS_node


class TWnode(TNS_node.node):
    def __init__(self, nodeName: str = "N000"):
        super().__init__(nodeName)
        self.version = TCS_utils.version()
        self.description = "App description"
        # read from csv

        self.app_config_list = TCS_configApp.TAS_apps_config(nodeName).configs
        # dlog system config
        self.interface.dlog_multiline(str(self._config), "SYSTEM-CONFIG")

        # dlog app Config
        for i in self.app_config_list:
            self.interface.dlog_multiline(str(i), str(i.app_code + "-CONFIG"))

        # handle remote and local apps
        self._local_app_config_list = []
        self._remote_app_config_list = []
        self._filter_apps()

        self.interface.dlog("Adding Local Apps", "info")
        self._add_app(self._local_app_config_list)
        if self._config.system.remote_app_enabled:
            self.interface.dlog("Adding Remote Apps", "info")
            self._add_app(self._remote_app_config_list)
        else:
            self.interface.log("REMOTE APPS DISABLE", "NOTICE")
        # self.add_app(TMSapp_MDYP)

    def _filter_apps(self):
        for app in self.app_config_list:
            if app.local_app:
                self._local_app_config_list.append(app)
            elif not app.local_app:
                self._remote_app_config_list.append(app)

    def _add_app(self, app_list):
        if not self._config.system.test_mode:
            for i in app_list:
                if i.active:
                    self._app_import(i)
        else:
            for i in app_list:
                if i.active_test:
                    self._app_import(i)

    def _app_import(self, app):
        self._sys_path(app)
        temp_app = importlib.import_module(app.main_app)
        self.add_app(temp_app, app)

    def _sys_path(self, app_info):
        if app_info.local_app:
            sys.path.append(os.path.join(TCS_variables.PYBIRD_DIRECTORIES.APP_LOCAL, app_info.app_code))
        elif not app_info.local_app:
            sys.path.append(os.path.join(TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_REMOTE_APP_DIRECTORY, app_info.app_code))

    def myStart(self):
        pass

    def myStep(self):
        pass

    def myShutdown(self):
        pass


if __name__ == "__main__":
    sys.path.append(os.path.join(os.environ["PYBIRD"], "src"))
    h = TWnode()
    h._start()
    h.step()
