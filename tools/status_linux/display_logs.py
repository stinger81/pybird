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
import sys

sys.path.append(os.path.join(os.environ["PYBIRD"], "src"))
import TCS_variables as VAR
import TCS_config

logs = os.listdir(VAR.PYBIRD_DATA_LOG_DIRECTORY)

config = TCS_config.TCS_config()

report_len = config.status.log_length

for l in logs:

    temp_path = os.path.join(VAR.PYBIRD_DATA_LOG_DIRECTORY, l)
    if os.path.isdir(temp_path):
        report = os.listdir(temp_path)
    else:
        with open(temp_path, "r") as f:
            report = f.readlines()
    print(l + " -> Total Log Messages: " + str(len(report)))
    if report == []:
        print("No Log Messages (" + l + ")")
    elif (len(report) < report_len):
        for i in range(len(report)):
            print(report[i].strip())
    else:
        for i in range(report_len):
            print(report[-report_len + i].strip())

    print()
