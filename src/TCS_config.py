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

"""
Configuration Manager
handles all file processing for config directory

"""
import os
import sys

import toml

import TCS_variables


class TCS_config:
    def __init__(self):
        self._config = None
        if "-boot" in sys.argv:
            try:
                self.file = os.path.join(TCS_variables.HOME, "PYBIRD_SERVER_CONFIG.toml")
                self._fullConfig = toml.load(self.file)
                self._config = self._fullConfig["system_config"]
            except:
                pass
        if self._config == None:
            try:
                self.file = os.path.join(TCS_variables.HOME, "PYBIRD_SERVER_CONFIG.toml")
                self._fullConfig = toml.load(self.file)
                self._config = self._fullConfig["system_config"]
            except:
                self.file = os.path.join(TCS_variables.PYBIRD_CONFIG_DIRECTORY, "PYBIRD_SERVER_CONFIG.toml")
                self._fullConfig = toml.load(self.file)
                self._config = self._fullConfig["system_config"]

        self._agrv = None

        self.system: system_config = system_config()
        self.logging: logging_config = logging_config()
        self.console: console_config = console_config()
        self.twitter: twitter_config = twitter_config()
        self.platform: platform = platform()
        self.status: status = status()
        self.encryption: encryption = encryption()
        self.credentials: credentials = credentials()

        self._read_config()
        self._read_sys_argv()

        if self.platform.force_test_mode:
            self.system.test_mode = True

        if self.system.test_mode:
            self.system.debug_mode = True

        if not self.logging.enable_master_log and not self.logging.enable_session_log:
            self.logging.enable_session_log = True

    def _read_config(self):
        # file = open(self.file, "r")
        # self._config = json.load(file)
        # file.close()

        self.system._read(self._config)
        self.logging._read(self._config)
        self.console._read(self._config)
        self.twitter._read(self._config)
        self.status._read(self._config)
        self.encryption._read(self._config)
        self.credentials._read(self._config)

    def _read_sys_argv(self):
        self._agrv = sys.argv

        for arg in self._agrv:
            if arg == "-test" or arg == "-t":
                self.system.test_mode = True
            elif arg == "-debug" or arg == "-d":
                self.system.debug_mode = True
            elif arg == "-null_test":
                self.system.test_mode = False
            elif arg == "-null_debug":
                self.system.debug_mode = False
            elif arg == "-aws_test":
                self.platform.has_cli = False
                self.system.debug_mode = False
                self.system.test_mode = False
            elif arg == "-null_aws":
                self.platform.has_cli = True
            elif arg == "-boot":
                self.platform.has_cli = False
                self.system.test_mode = False
                self.system.debug_mode = False
            elif arg == "-null_boot":
                self.platform.has_cli = True

    def __str__(self) -> str:
        string_out = ""
        string_out += f"system: \n{self.system}\n"
        string_out += f"console: \n{self.console}\n"
        string_out += f"twitter: \n{self.twitter}\n"
        string_out += f"platform: \n{self.platform}\n"
        string_out += f"status: \n{self.status}\n"
        string_out += f"encryption: \n{self.encryption}\n"
        return string_out


class system_config:
    def __init__(self) -> None:
        self._raw = None

        self.test_mode = False
        self.debug_mode = False
        self.remote_app_enabled = False

    def _read(self, _config):
        self._raw = _config["system"]

        self.test_mode = self._raw["test_mode"]
        self.debug_mode = self._raw["debug_mode"]
        self.remote_app_enabled = self._raw["remote_app_enabled"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"test_mode: {self.test_mode}\n"
        string_out += f"debug_mode: {self.debug_mode}\n"
        string_out += f"remote_app_enabled: {self.remote_app_enabled}\n"

        return string_out


class logging_config:
    def __init__(self) -> None:
        self._raw = None

        self.enable_master_log = False
        self.enable_session_log = True
        self.enable_app_log = False

        self.master_log_length = 250000
        self.session_log_length = -1
        self.app_log_length = 100000

    def _read(self, _config):
        self._raw = _config["logging"]

        self.enable_master_log = self._raw["enable_master_log"]
        self.enable_session_log = self._raw["enable_session_log"]
        self.enable_app_log = self._raw["enable_app_log"]
        self.master_length = self._raw["master_log_length"]
        self.session_length = self._raw["session_log_length"]
        self.app_length = self._raw["app_log_length"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"enable_master_log: {self.enable_master_log}\n"
        string_out += f"enable_session_log: {self.enable_session_log}\n"
        string_out += f"enable_app_log: {self.enable_app_log}\n"
        string_out += f"master_length: {self.master_length}\n"
        string_out += f"session_length: {self.session_length}\n"
        string_out += f"app_length: {self.app_length}\n"

        return string_out


class console_config:
    def __init__(self) -> None:
        self._raw = None

        self.mode: str = "unknown"
        self.show_console: bool = True

    def _read(self, _config):
        self._raw = _config["console"]

        self.show_console = self._raw["show_console"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"show_console: {self.show_console}\n"

        return string_out


class twitter_config:
    def __init__(self) -> None:
        self._raw = None

        self.max_char: int = 280

    def _read(self, _config):
        self._raw = _config["twitter"]

        self.max_char = self._raw["max_char"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"max_char: {self.max_char}\n"
        return string_out


class platform:
    def __init__(self) -> None:
        self.has_cli = TCS_variables.PLATFORM_HAS_CLI
        self.force_test_mode = TCS_variables.PLATFORM_FORCE_TEST_MODE

    def __str__(self) -> str:
        string_out = ""
        string_out += f"has_cli: {self.has_cli}\n"
        string_out += f"force_test_mode: {self.force_test_mode}\n"
        return string_out


class status:
    def __init__(self) -> None:
        self._raw = None
        self.log_length = None

    def _read(self, _config):
        self._raw = _config["status"]
        self.log_length = self._raw["log_length"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"log_length: {self.log_length}\n"
        return string_out


class encryption:
    def __init__(self) -> None:
        self._raw = None
        self.encrypt_app_key = None

    def _read(self, _config):
        self._raw = _config["encryption"]
        self.encrypt_app_key = self._raw["encrypt_app_keys"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"encrypt_app_key: {self.encrypt_app_key}\n"
        return string_out


class credentials:
    def __init__(self) -> None:
        self._raw = None
        self.delete_dir_after_upload = True
        self.delete_file_after_upload = True

    def _read(self, _config):
        self._raw = _config["credentials"]
        self.delete_dir_after_upload = self._raw["delete_dir_after_upload"]
        self.delete_file_after_upload = self._raw["delete_file_after_upload"]

    def __str__(self) -> str:
        string_out = ""
        string_out += f"delete_dir_after_upload: {self.delete_dir_after_upload}\n"
        string_out += f"delete_file_after_upload: {self.delete_file_after_upload}\n"
        return string_out


if __name__ == "__main__":
    test = TCS_config()
