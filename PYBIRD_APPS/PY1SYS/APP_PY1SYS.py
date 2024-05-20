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

import TAS_app_local
import TCS_configApp
import TCS_utils
import TCS_variables


class TUAapp(TAS_app_local.app):
    def __init__(self, parameters: TCS_configApp._app_config, test: bool = False):
        super().__init__("PY1SYS", parameters, test)
        self.name = "PY1SYS"
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
        header = ["Timestamp", "ISO Time", "CPU %", "Memory Used %", "Memory Used (Bytes)", "Memory Free (Bytes)",
                  "Disk Used %", "Disk Used (Bytes)", "Disk Free (Bytes)", "Appdata Size (Bytes)",
                  "Session Size (Bytes)", "Log Data Size (Bytes)", "Log Export Size (Bytes)"]
        report = []
        data = [datetime.datetime.utcnow().timestamp(),
                datetime.datetime.utcnow().isoformat()]
        report.append("*** START OF REPORT ***")

        cpu = self._get_cpu_usage()
        report.append(f"CPU Usage: {cpu}%")
        data.append(cpu)

        percent, used, free = self._get_memory_usage()
        report.append(f"Memory Used: {percent}% | Used: {str(used)} | Free: {str(free)}")
        data.append(percent)
        data.append(int(used))
        data.append(int(free))

        percent, used, free = self._get_disk_usage_total()
        report.append(f"Disk Used: {percent}% | Used: {str(used)} | Free: {str(free)}")
        data.append(percent)
        data.append(int(used))
        data.append(int(free))

        data_appdata = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.DATA_APPDATA)
        report.append(f"Data Appdata Size: {str(data_appdata)}")
        data.append(int(data_appdata))

        data_session = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.DATA_SESSION)
        report.append(f"Data Session Size: {str(data_session)}")
        data.append(int(data_session))

        data_log = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.DATA_LOG)
        report.append(f"Data Log Size: {str(data_log)}")
        data.append(int(data_session))

        export_log = self.get_dir_size(TCS_variables.PYBIRD_DIRECTORIES.LOG)
        report.append(f"Export Log Size: {str(export_log)}")
        data.append(int(export_log))

        report.append("**** END OF REPORT ****")
        self.interface.log_list(report, "REPORT")

        if not self.file_interface.exists(self.save_file):
            with self.file_interface.open(self.save_file,"w", newline="") as f:
                csv_file = csv.writer(f)
                csv_file.writerow(header)

        with self.file_interface.open(self.save_file, 'a',newline="") as f:
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
