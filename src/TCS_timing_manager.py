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
import time

import TCS_configApp

day_codes: dict = {
    "M": 0,
    "T": 1,
    "W": 2,
    "R": 3,
    "F": 4,
    "S": 5,
    "U": 6
}


class TimingManager:
    def __init__(self, name, parameters: TCS_configApp._app_config):
        self._app_config: TCS_configApp._app_config = parameters
        self.name: str = self._app_config.app_code
        self.mode = self._app_config.timing_mode
        self.step_duration = self._app_config.timing_step_duration
        self.step_sync_time = self._app_config.timing_step_sync_time
        self.timing_time_list = self._app_config.timing_time_list
        self.timing_once = self._app_config.timing_once

        self.last_time = datetime.datetime.utcnow()

        self._start_complete = False

        if self.mode == 'test':
            self._next_time = self._next_time_test
            self.last_time = self.last_time - datetime.timedelta(seconds=60)
        elif self.mode == 'step':
            self._next_time = self._next_time_step
            self.step_duration = self._step_duration_decode(self.step_duration)
            if self.step_sync_time != "":
                self.temp_time = datetime.datetime.strptime(self.step_sync_time, "%d %b %Y %H:%M:%S")
                delta = datetime.datetime.utcnow().timestamp() - self.temp_time.timestamp()
                mult = delta // self.step_duration
                self.last_time = self.temp_time + datetime.timedelta(seconds=self.step_duration * mult)
        elif self.mode == 'time':
            self._next_time = self._next_time_time
        elif self.mode == 'cont':
            self._next_time = self._next_time_cont
        elif self.mode == 'request':
            self._next_time = self._next_time_request
        elif self.mode == 'start':
            self._next_time = self._next_time_start
        elif self.mode == 'once':
            self._next_time = self._next_time_once
        else:
            raise ValueError(f"Invalid mode: {self.mode}")


    def get_cur_time(self):
        """
        Get the current step time
        :return:
        """
        return self.last_time

    def set_next_time(self):
        """
        Set the next time
        :return:
        """
        next_time = self._next_time()
        self.last_time = next_time
        return next_time

    def _next_time_test(self):
        """
        Get the next time for the test mode
        :return:
        """
        return self.last_time + datetime.timedelta(seconds=60)

    def _next_time_step(self):
        """
        Get the next time for the step mode
        :return:
        """
        if self._app_config.timing_step_skip_missed:
            delta = datetime.datetime.utcnow().timestamp() - self.last_time.timestamp()
            if delta < self.step_duration:
                return self.last_time + datetime.timedelta(seconds=self.step_duration)
            else:
                mult = delta // self.step_duration
                return self.last_time + datetime.timedelta(seconds=self.step_duration * (mult + 1))
        else:
            return self.last_time + datetime.timedelta(seconds=self.step_duration)

    def _next_time_time(self):
        """
        Get the next time for the time mode
        :return:
        """
        # build a list of times
        time_list = []
        for time in self.timing_time_list:
            split_time = time.split()
            my_time = datetime.datetime.strptime(split_time[0], "%H:%M:%S")
            now = datetime.datetime.utcnow()
            my_time = my_time.replace(year=now.year, month=now.month, day=now.day)
            if split_time[1] in day_codes:
                delta = day_codes[split_time[1]] - my_time.weekday()

                if delta == 0:
                    if my_time.timestamp() < now.timestamp():
                        delta += 7
                elif delta < 0:
                    delta += 7

                my_time = my_time + datetime.timedelta(days=delta)
                time_list.append(my_time)
            elif split_time[1] == "E":
                if my_time.timestamp() < now.timestamp():
                    my_time = my_time + datetime.timedelta(days=1)
                time_list.append(my_time)
        time_list.sort()
        for time in time_list:
            if time.timestamp() > self.last_time.timestamp():
                return time

    def _next_time_cont(self):
        """
        Get the next time for the cont mode
        :return:
        """
        return self.last_time

    def _next_time_request(self):
        """
        Get the next time for the request mode
        :return:
        """
        return 'request'

    def _next_time_once(self):
        """
        Get the next time for the once mode
        :return:
        """
        my_time = datetime.datetime.strptime(self.timing_once, "%d %b %Y %H:%M:%S")
        if my_time.timestamp() > datetime.datetime.utcnow().timestamp():
            return my_time
        return 'never'

    def _next_time_start(self):
        """
        Get the next time for the start mode
        :return:
        """
        if not self._start_complete:
            self._start_complete = True
            return datetime.datetime.utcnow()
        return 'never'


    def _step_duration_decode(self, duration: str):
        """
        Decode the step duration
        :param duration:
        :return:
        """
        accepted_vals = "dhms"
        split_time = duration.split()
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


class test_config:
    app_code = "test"
    timing_mode = "time"
    timing_step_duration = "1 s"
    timing_step_skip_missed = False
    timing_step_sync_time = "1 Mar 2024 00:00:00"
    timing_time_list = ["11:00:00 W",
                        "12:00:00 R",
                        "13:00:00 F",
                        "14:00:00 S",
                        "15:00:00 U",
                        "16:00:00 M",
                        "17:00:00 T",
                        "18:00:00 E"]


if __name__ == "__main__":
    test = TimingManager("", test_config())
    for i in range(1):
        print(test.set_next_time())
        print(datetime.datetime.utcnow())
        time.sleep(2)
