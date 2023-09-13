#!/bin/bash
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

#export HOME="home/ec2-user"
#tag=$( tail -n 1 $HOME/last_boot.txt )
# echo "last boot: $tags"

python3 $PYBIRD/tools/status_linux/boot_time.py
python3 $PYBIRD/tools/status_linux/uptime.py

echo "Services /etc/systemd/system"
echo "PYBIRD_run service"
systemctl status PYBIRD_run
echo " "
while getopts 'l:' OPTION; do
    case "$OPTION" in
        l)
            echo "Log Messages"
            python $PYBIRD/tools/status_linux/display_logs.py
            ;;
        ?)
            echo "script usage: $(basename \$0) [-l] " >&2
            exit 1
            ;;
    esac
done
shift "$(($OPTIND -1))"
