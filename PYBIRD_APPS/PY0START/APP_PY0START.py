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

import psutil
import os
import csv
from pathlib import Path

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

        self.description = "System Start Monitor App"

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
        header = ["Timestamp", "ISO Time", "Session ID", "Pybird Version", "Pybird Dir Size (Bytes)",
                  ".pybird Dir Size (Bytes)", "Remote Dir Size (Bytes)"]
        report = []
        data = [datetime.datetime.utcnow().timestamp(),
                datetime.datetime.utcnow().isoformat()]
        # start of report
        report.append("*** START OF REPORT | ID: STARTUP ***")
        # ession ID
        report.append(f"Session ID: {self.interface.sessionID}")
        data.append(self.interface.sessionID)

        # Pybird Version
        report.append(f"Pybird Version: {TCS_utils.version().full_str()}")
        data.append(TCS_utils.version().full_str())

        # Pybird Directory Size
        pybird_dir_size = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_DIRECTORY)
        report.append(f"Pybird Dir Size: {str(pybird_dir_size)}")
        data.append(int(pybird_dir_size))

        # .pybird Directory Size
        _pybird_dir_size = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_HOME)
        report.append(f".pybird Dir Size: {str(_pybird_dir_size)}")
        data.append(int(_pybird_dir_size))

        # Remote Dir Size
        if TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_REMOTE_APP_DIRECTORY != str(Path.home()):
            remote_dir_size = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_REMOTE_APP_DIRECTORY)
        else:
            remote_dir_size = -1
        report.append(f"Remote Dir Size: {str(remote_dir_size)}")
        data.append(int(remote_dir_size))

        report.append("**** END OF REPORT | ID: STARTUP ****")
        self.interface.log_list(report, "REPORT")

        if not self.file_interface.exists("startup.csv"):
            with self.file_interface.open("startup.csv","w", newline="") as f:
                csv_file = csv.writer(f)
                csv_file.writerow(header)

        with self.file_interface.open("startup.csv", 'a',newline="") as f:
            csv_file = csv.writer(f)
            csv_file.writerow(data)

    def _get_cpu_usage(self) -> float:
        """
        Get CPU usage
        :return:
        """
        return psutil.cpu_percent(interval=1)

    def _get_memory_usage(self) -> tuple[float, TCS_utils.ByteSize, TCS_utils.ByteSize]:
        """
        Get memory usage
        :return:
        percent
        total used
        total free
        """
        my_read = psutil.virtual_memory()
        percent = my_read.percent
        used = TCS_utils.ByteSize(my_read.used)
        free = TCS_utils.ByteSize(my_read.free)
        return percent, used, free

    def _get_disk_usage_total(self) -> tuple[float, TCS_utils.ByteSize, TCS_utils.ByteSize]:
        """
        get disk usage
        :return:
        """
        my_read = psutil.disk_usage('/')
        percent = my_read.percent
        used = TCS_utils.ByteSize(my_read.used)
        free = TCS_utils.ByteSize(my_read.free)
        return percent, used, free

    def get_dir_size(self, path) -> TCS_utils.ByteSize:
        total = 0
        with os.scandir(path) as d:
            for f in d:
                if f.is_file():
                    total += f.stat().st_size
                elif f.is_dir():
                    total += self.get_dir_size(f.path)
        return TCS_utils.ByteSize(total)


if __name__ == "__main__":
    app = TMSapp()
    app._run()
    app.step()