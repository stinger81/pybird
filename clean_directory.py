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

import os
import shutil

TEMP_LIST = ["__pycache__", "log", "data", "__temp__"]


def remove_pybird_temp_directories(root_directory):
    for root, dirs, files in os.walk(root_directory):
        for directory in dirs:
            if directory in TEMP_LIST:
                dir_path = os.path.join(root, directory)
                print(f"Removing directory: {dir_path}")
                try:
                    # Remove the directory
                    # os.rmdir(dir_path)
                    shutil.rmtree(dir_path)

                except OSError as e:
                    print(f"Error while removing directory: {e}")


if __name__ == "__main__":
    # Specify the root directory where you want to remove Python cache directories
    root_directory = os.getcwd()
    # Call the function to remove pybird temp directories
    remove_pybird_temp_directories(root_directory)
