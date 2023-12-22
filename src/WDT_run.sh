#!/bin/bash
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

_HOME="/home/user"
PYBIRD="$_HOME/pybird"
WDT="$PYBIRD/src"

export WDT_LOGFILE="$_HOME/WDT_ERROR_LOG.log"

# Reboot threshold - software will attempt to reboot machine (depends on permissions)
# If set to zero, no reboot
reboot_threshold=2
reboot_command='sudo reboot'

_py_command='python3'
_py_file_name='WDT_watch.py'

crashes=0

echo "WDT_run.sh -> V0_8_3-DEV"
echo "Watch Dog Service Starting $(date)" >> $WDT_LOGFILE
echo "Entering WDT startup delay"
sleep 90
echo "Launching WDT: $(date)" >> $WDT_LOGFILE
while true; do
    echo "Launching Python WDT"
    $_py_command $WDT/$_py_file_name

    
    #increment crashes
    crashes=$((crashes+1))
    echo "crashes: $crashes"

    if [ $reboot_threshold -ne 0 ]; then
        n=$((crashes%$reboot_threshold))
        if [ $n -eq 0 ]; then
            # Reboot
            echo 'Crashes exceed reboot threshold - rebooting' >> $WDT_LOGFILE
            echo "Watch Dog Service TERMINATED" >> $WDT_LOGFILE
            $reboot_command
        fi
    fi
    

    sleep 60



done

echo "Watch Dog Service TERMINATED" >> $WDT_LOGFILE