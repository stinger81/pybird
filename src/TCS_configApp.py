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

import csv
import json
import os

import TCS_utils
import TCS_variables


class TAS_apps_config:
    """
    read from the app config CSV file
    """

    def __init__(self, nodeName="N000") -> None:
        self.version = TCS_utils.version()
        self.file = os.path.join(
            TCS_variables.PYBIRD_CONFIG_DIRECTORY,
            str(nodeName + TCS_variables.PYBIRD_NODE_CONFIG_ENDING))

        self.configs: list[_app_config] = []

        self._read_config_csv()
        self._read_config_json()
        self._post_process_config()

    def _read_config_csv(self):
        # read configuration file
        with open(self.file, mode='r', encoding='UTF-8', newline='') as config_file:
            # print(config_file)
            csv_read = csv.reader(config_file)
            i = 0
            for row in csv_read:
                # print(row)
                if i != 0:
                    self.configs.append(_app_config())
                    self.configs[-1]._csv = row
                    if row[1][0] == "#":
                        self.configs[-1].active = False
                    else:
                        self.configs[-1].active = TCS_utils.str_to_bool(row[1])

                    if row[2][0] == "#":
                        self.configs[-1].active_test = False
                    else:
                        self.configs[-1].active_test = TCS_utils.str_to_bool(row[2])

                    if row[0][0] == "#":
                        self.configs[-1].app_code = row[0][1:]
                        self.configs[-1]._full_disable = True
                        self.configs[-1].active = False
                        self.configs[-1].active_test = False
                    else:
                        self.configs[-1].app_code = row[0]

                    self.configs[-1].local_app = TCS_utils.str_to_bool(row[3])
                    self.configs[-1].csv_debug_mode = TCS_utils.str_to_bool(row[4])
                    self.configs[-1].main_app = row[5]
                    self.configs[-1].app_config = row[6]
                    self.configs[-1].dependencies = TCS_utils.delimitated_to_list_str(row[7], "|")
                    self.configs[-1].DB_dedicated_access = TCS_utils.str_to_bool(row[8])
                    self.configs[-1].DB_dedicated_name = row[9]
                    self.configs[-1].DB_shared_access = TCS_utils.str_to_bool(row[10])
                    self.configs[-1].DB_shared_name = row[11]

                    # print(self.configs[-1])
                i += 1

    def _read_config_json(self):
        for config in self.configs:
            if not config._full_disable:
                if config.local_app:
                    json_address = os.path.join(TCS_variables.PYBIRD_APP_LOCAL_DIRECTORY, config.app_code,
                                                config.app_config)
                else:
                    json_address = os.path.join(TCS_variables.PYBIRD_REMOTE_APP_DIRECTORY, config.app_code,
                                                config.app_config)
                # print(json_address)
                with open(json_address, "r") as json_file:
                    config._json = json.load(json_file)
                    config.step_time = TAS_apps_config.step_time_handle(config._json["step_time"])
                    config.step_on_boot = config._json["step_on_boot"]
                    config.step_on_shutdown = config._json["step_on_shutdown"]
                    config.json_debug_mode = config._json["debug_mode"]
                    config.app_parameters = config._json["app_parameters"]
                    config.log_to_DB = config._json["log_to_DB"]
                    config.checksum_sha256 = config._json["checksum_sha256"]

    def _post_process_config(self):
        for config in self.configs:
            if config.csv_debug_mode or config.json_debug_mode:
                config.debug_mode = True
            elif TCS_variables.PLATFORM_FORCE_DEBUG_MODE:
                config.debug_mode = True

    @staticmethod
    def step_time_handle(in_step_time: str):
        accepted_vals = "dhms"
        split_time = in_step_time.split()
        if len(split_time) == 1:
            if split_time[0][-1] in accepted_vals:
                split_time.append(split_time[0][-1])
                split_time[0] = split_time[0][:-1]
            else:
                split_time.append("s")
        if split_time[1] == "d":
            return int(split_time[0]) * 24 * 60 * 60
        elif split_time[1] == "h":
            return int(split_time[0]) * 60 * 60
        elif split_time[1] == "m":
            return int(split_time[0]) * 60
        else:
            return int(split_time[0])


class _app_config:
    """
    class that acts as a struct data structure
    Only Stores Data
    """

    def __init__(self) -> None:
        # csv
        self._csv: list = []
        self._full_disable: bool = False
        self.app_code: str = "unknown"
        self.active: bool = False
        self.active_test: bool = False
        self.local_app: bool = True
        self.csv_debug_mode: bool = False
        self.main_app: str = "unknown"
        self.app_config: str = "unknown"
        self.dependencies: list[str] = ["unknown"]
        self.DB_dedicated_access: bool = False
        self.DB_dedicated_name: str = "unknown"
        self.DB_shared_access: bool = False
        self.DB_shared_name: str = "unknown"
        # json
        self._json: dict = {}
        self.json_debug_mode: bool = False
        self.step_time: int = 0  # seconds
        self.step_on_boot: bool = False
        self.step_on_shutdown: bool = False
        self.app_parameters: dict = {}
        self.log_to_DB: bool = False
        self.checksum_sha256: str = ""
        # post processing
        self.debug_mode: bool = False

    def __str__(self) -> str:
        string_out = ""
        string_out += "_csv: " + str(self._csv) + "\n"
        string_out += "_full_disable: " + str(self._full_disable) + "\n"
        string_out += "active: " + str(self.active) + "\n"
        string_out += "active_test: " + str(self.active_test) + "\n"
        string_out += "local_app: " + str(self.local_app) + "\n"
        string_out += "csv_debug_mode: " + str(self.csv_debug_mode) + "\n"
        string_out += "main_app: " + str(self.main_app) + "\n"
        string_out += "app_config: " + str(self.app_config) + "\n"
        string_out += "dependencies: " + str(self.dependencies) + "\n"
        string_out += "_json: " + str(self._json) + "\n"
        string_out += "json_debug_mode: " + str(self.json_debug_mode) + "\n"
        string_out += "step_time: " + str(self.step_time) + "\n"
        string_out += "step_on_boot: " + str(self.step_on_boot) + "\n"
        string_out += "step_on_shutdown: " + str(self.step_on_shutdown) + "\n"
        string_out += "app_parameters: " + str(self.app_parameters) + "\n"
        string_out += "checksum_sha256: " + str(self.checksum_sha256) + "\n"
        string_out += "debug_mode: " + str(self.debug_mode) + "\n"

        return string_out
