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


import multiprocessing
from typing import List

from TBS_bootloader_vars import *

time.sleep(0.5)

PROCESS: List[multiprocessing.Process] = []

def launchNodes():
    """
    Launch all nodes
    :return:
    """
    for node in os.environ["PYBIRDnodes"].split("|"):
        _launchNode(node)


def _launchNode(nodeName: str, daemon: bool = False):
    """
    Launch a node
    :param nodeName:
    :param daemon:
    :return:
    """
    import TNS_run  # DO NOT MOVE
    PROCESS.append(multiprocessing.Process(name=nodeName,
                                           target=TNS_run.run,
                                           args=(nodeName, True,),  # comma required after vars
                                           daemon=daemon))
    PROCESS[-1].start()


def watchdog():
    """
    Watchdog for nodes
    :return:
    """
    while True:
        for i in range(len(PROCESS)):
            # print(PROCESS[i].pid)
            if not PROCESS[i].is_alive():
                p = PROCESS.pop(i)
                print("Processing Crash[" + p.name + "]")
                p.terminate()
                _launchNode(p.name)
                del p
                break
        time.sleep(1)


def shutdown():
    """
    Shutdown all nodes
    :return:
    """
    for p in PROCESS:
        p.kill()
    exit()


if __name__ == "__main__":
    launchNodes()
    if CONFIG["watchdog"]["launchSWwdt"]:
        watchdog()
    else:
        while True:
            for p in PROCESS:
                if not p.is_alive():
                    shutdown()
