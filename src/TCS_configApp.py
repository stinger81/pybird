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

import csv
import os

import toml

import TCS_utils
import TCS_variables


class TAS_apps_config:
    """
    read from the app config CSV file
    """

    def __init__(self, nodeName="N000") -> None:
        self.version = TCS_utils.version()
        self.file = os.path.join(
            TCS_variables.PYBIRD_DIRECTORIES.CONFIG,
            str(nodeName + TCS_variables.FILE_EXTENSIONS.NODE_CONFIG))

        self.configs: list[_app_config] = []

        self._read_config_csv()
        self._read_configtoml()
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
                    # self.configs[-1].DB_dedicated_access = TCS_utils.str_to_bool(row[8])
                    # self.configs[-1].DB_dedicated_name = row[9]
                    # self.configs[-1].DB_shared_access = TCS_utils.str_to_bool(row[10])
                    # self.configs[-1].DB_shared_name = row[11]

                    # print(self.configs[-1])
                i += 1

    def _read_configtoml(self):
        for config in self.configs:
            if not config._full_disable:
                if config.local_app:
                    toml_address = os.path.join(TCS_variables.PYBIRD_DIRECTORIES.APP_LOCAL, config.app_code,
                                                config.app_config)
                else:
                    toml_address = os.path.join(TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_REMOTE_APP_DIRECTORY, config.app_code,
                                                config.app_config)
                # print(json_address)
                with open(toml_address, "r") as toml_file:
                    config.toml = toml.load(toml_file)

                    config.load_before_each_step = config.toml["app_config"]["load_before_each_step"]
                    config.save_after_each_step = config.toml["app_config"]["save_after_each_step"]

                    config.timing_mode = config.toml["app_config"]["timing"]["mode"]
                    config.timing_step_duration = config.toml["app_config"]["timing"]["step"]["step_duration"]
                    config.timing_step_skip_missed = config.toml["app_config"]["timing"]["step"]["skip_missed"]
                    config.timing_step_sync_time = config.toml["app_config"]["timing"]["step"]["sync_time"]
                    config.timing_time_list = config.toml["app_config"]["timing"]["time"]["time_list"]
                    
                    config.toml_debug_mode = config.toml["app_config"]["debug_mode"]
                    config.save_key = config.toml["app_config"]["save_key"]



                    config.atlas_dbs_enabled = config.toml["app_config"]["atlas"]["enabled"]
                    config.log_to_DB_enabled = config.toml["app_config"]["atlas"]["logging"]["enabled"]
                    config.log_to_DB_name = config.toml["app_config"]["atlas"]["logging"]["DB_Name"]

                    config.app_parameters = config.toml["app_parameters"]
                    # config.database_primary_active = config.toml["app_config"]["atlas_databases"]["primary"]["active"]
                    # config.database_primary_name = config.toml["app_config"]["atlas_databases"]["primary"]["DB_Name"]
                    # config.log_to_DB = config.toml["app_config"]["atlas_databases"]["primary"]["log_to_DB"]
                    # config.database_secondary_active = config.toml["app_config"]["atlas_databases"]["secondary"]["active"]
                    # config.database_secondary_name = config.toml["app_config"]["atlas_databases"]["secondary"]["DB_Name"]

    def _post_process_config(self):
        for config in self.configs:
            if config.csv_debug_mode or config.toml_debug_mode:
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

        self.toml: dict = {}
        self.toml_debug_mode: bool = False
        self.load_before_each_step: bool = False
        self.save_after_each_step: bool = False
        self.timing_mode = "unknown"
        self.timing_step_duration = "1 m"
        self.timing_step_skip_missed = True
        self.timing_step_sync_time = ""
        self.timing_time_list = []
        self.save_key:str = ""
        self.app_parameters: dict = {}
        self.atlas_dbs_enabled: bool = False
        self.log_to_DB_enabled: bool = False
        self.log_to_DB_name: str = ""
        # self.database_primary_active = False
        # self.database_primary_name = ""
        # self.log_to_DB = False
        # self.database_secondary_active = False
        # self.database_secondary_name = False
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
        string_out += "toml: " + str(self.toml) + "\n"
        string_out += "toml_debug_mode: " + str(self.toml_debug_mode) + "\n"
        string_out += "load_before_each_step: " + str(self.load_before_each_step) + "\n"
        string_out += "save_after_each_step: " + str(self.save_after_each_step) + "\n"
        string_out += "timing_mode: " + str(self.timing_mode) + "\n"
        string_out += "timing_step_duration: " + str(self.timing_step_duration) + "\n"
        string_out += "timing_step_skip_missed: " + str(self.timing_step_skip_missed) + "\n"
        string_out += "timing_step_sync_time: " + str(self.timing_step_sync_time) + "\n"
        string_out += "timing_time_list: " + str(self.timing_time_list) + "\n"
        string_out += "app_parameters: " + str(self.app_parameters) + "\n"
        string_out += "atlas_dbs_enabled: " + str(self.atlas_dbs_enabled) + "\n"
        string_out += "log_to_DB_enabled: " + str(self.log_to_DB_enabled) + "\n"
        string_out += "log_to_DB_name: " + str(self.log_to_DB_name) + "\n"
        string_out += "debug_mode: " + str(self.debug_mode) + "\n"

        return string_out
