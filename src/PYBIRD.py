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


import importlib
import os
import sys

import TCS_utils
import TCS_variables
import TNS_run


def pre_start():
    """
    Check for help and version flags
    Set systems environment variables
    :return:
    """
    for i in range(len(sys.argv)):
        # check for help and version flags
        if sys.argv[i] in TCS_variables.SYS_ARG.HELP:
            print(TCS_variables.HELP)
            exit(0)
        elif sys.argv[i] in TCS_variables.SYS_ARG.VERSION:
            print(TCS_utils.version())
            exit(0)
        # set systems environment variables
        elif sys.argv[i] in TCS_variables.SYS_ARG.REMOTE:
            os.environ[TCS_variables.PYBIRD_ENV.REMOTE_DIR_TAG] = sys.argv[i + 1]
            importlib.reload(TCS_variables)
        elif sys.argv[i] in TCS_variables.SYS_ARG.PLATFORM:
            os.environ[TCS_variables.PYBIRD_ENV.PLATFORM_TAG] = sys.argv[i + 1]
            importlib.reload(TCS_variables)


def launch_node(node_name: str):
    """
    Launch a node
    :param node_name:
    :return:
    """
    node = TNS_run.run(node_name)
    node.start()
    # print(f"Starting Node {node_name}")
    node.run()


def launch_app(app_name: str):
    # create temp config
    dir = os.path.join(TCS_variables.PYBIRD_DIRECTORIES.CONFIG, "TEMP_NODE_CONFIG.csv")
    local = False
    if os.path.exists(os.path.join(TCS_variables.PYBIRD_DIRECTORIES.APP_LOCAL, app_name.upper())):
        local = True
    with open(dir, "w") as f:
        f.write("App Code (4 Char),Active(bool),Test Active (bool),Local App (bool),Debug Mode (bool),Main File(str),"
                "Config file name,Dependent Files('|' separated\n")
        myStr: str = f"{app_name.upper()},true,true,{str(local).lower()},false,APP_{app_name.upper()},APP_{app_name.upper()}.toml,"
        f.write(myStr)

    launch_node("TEMP")


if __name__ == "__main__":
    pre_start()

    # handle nodes first
    node_name = "N000"  # default node name
    node_in_tag = False
    for node_flag in TCS_variables.SYS_ARG.NODE:
        if node_flag in sys.argv:
            node_name = sys.argv[sys.argv.index(node_flag) + 1]
            node_in_tag = True
            break
    # handle specific app launch
    app_name = "TEST"
    app_in_tag = False
    for app_flag in TCS_variables.SYS_ARG.APP:
        if app_flag in sys.argv:
            app_name = sys.argv[sys.argv.index(app_flag) + 1]
            app_in_tag = True
            break

    if node_in_tag and app_in_tag:
        raise TCS_variables.PYBIRDError("cannot launch node and app at same time")

    if node_in_tag:
        launch_node(node_name)
    elif app_in_tag:
        launch_app(app_name)
else:
    raise TCS_variables.PYBIRDError("PYBIRD.py cannot be imported")
