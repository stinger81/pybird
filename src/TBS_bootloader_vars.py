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
import sys
import time
from pathlib import Path

import toml

HOME = ""
for i in range(len(sys.argv)):
    if sys.argv[i] == "-boot":
        HOME = sys.argv[i + 1]
        break
if HOME == "":
    HOME = Path.home()


def joinToHome(path: str):
    paths = path.split("/")
    outPath = os.path.join(HOME, *paths)
    return outPath


SERVER_CONFIG_TOML = "PYBIRD_SERVER_CONFIG.toml"
# Read configuration file
CONFIG = toml.load(os.path.join(HOME, SERVER_CONFIG_TOML))  # will NOT launch if the file is not there
_PYBIRD = CONFIG["server"]["PYBIRD"]
_PYBIRDRemoteDir = CONFIG["server"]["PYBIRDRemoteDir"]
PYBIRDPlatform = CONFIG["server"]["PYBIRDPlatform"]
PYBIRDpython = CONFIG["server"]["PYBIRDpython"]

# build directories
PYBIRD = joinToHome(_PYBIRD)
PYBIRDRemoteDir = joinToHome(_PYBIRDRemoteDir)

# set environment
os.environ['PYBIRD'] = PYBIRD
os.environ['PYBIRDRemoteDir'] = PYBIRDRemoteDir
os.environ['PYBIRDPlatform'] = PYBIRDPlatform
os.environ['PYBIRDPython'] = PYBIRDpython

# get list of nodes to launch
nodes = CONFIG["nodes"]["nodes"]
try:
    node_env = nodes[0]
    for i in range(1, len(nodes)):
        node_env += "|"
        node_env += nodes[i]
except:
    node_env = "N000"

# add nodes to environment variables
os.environ["PYBIRDnodes"] = node_env

time.sleep(1)
