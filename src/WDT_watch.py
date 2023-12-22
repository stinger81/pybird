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

import os
import subprocess
import time
from datetime import datetime, timezone

import TCS_utils


class ServiceMonitor(object):

    def __init__(self, service):
        self.version = TCS_utils.version()

        self.service = service
        self.active = True
        self._error_file = os.environ["WDT_LOGFILE"]

        self._console(str("watchdog.py -> " + str(self.version)))

    def is_active(self):
        """Return True if service is running"""
        cmd = '/bin/systemctl status %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf8')
        stdout_list = proc.communicate()

        self.active = False
        for line in stdout_list[0].split('\n'):
            if 'Active:' in line:
                if '(running)' in line:
                    self.active = True
        if not self.active:
            self._write_crash(stdout_list)
        return self.active

    def _write_running(self, msg):
        pass

    def _write_crash(self, std_list):

        reportTime = str(datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S"))

        self._log("")
        self._log(str('START CRASH REPORT : ' + reportTime))
        # self._log(std_list)
        for group in std_list:

            if group == None:
                self._log("")

            else:
                for line in group.split("\n"):
                    self._log(line)

        self._log(str('END CRASH REPORT : ' + reportTime))
        self._log("")

        self._console(str(self.service + " CRASHED: " + reportTime))

    def start(self):
        cmd = '/bin/systemctl start %s.service' % self.service
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        proc.communicate()

        reportTime = str(datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S"))

        self._log("")
        self._log(str('START REBOOT REPORT : ' + reportTime))
        self._log(str(str(self.service) + ' RESTARTED'))
        self._log(str('END REBOOT REPORT : ' + reportTime))
        self._log("")

        self._console(str(self.service + " REBOOTED: " + reportTime))

    def _log(self, msg):
        with open(self._error_file, 'a') as f:
            f.write(str(msg) + '\n')

    def _console(self, msg):
        print(msg)


if __name__ == '__main__':
    watch = "TWIT_run"
    monitor = ServiceMonitor(watch)
    crash_threshold = 2
    crash = 0
    while True:
        if not monitor.is_active():
            monitor.start()
            crash += 1
        if crash == crash_threshold:
            break
        time.sleep(60)
