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

import atexit
import sys
import time
from signal import signal, SIGINT

import TCS_core
import TCS_interface
import TCS_utils
import TNS_node
import TNS_node_instance



class run(TCS_core.core):
    def __init__(self, NodeName, autoStart: bool = False) -> None:
        TCS_interface.write_state_file(nodeName=NodeName)
        super().__init__()
        self._host: TNS_node.node = TNS_node_instance.TWnode(NodeName)
        self.name = "RUN_" + self._host.name
        self.version = TCS_utils.version()
        self.description = "run class for nodes"

        self.interface.log(f"{self.name} v{self.version} : RUN-BASE INITIALIZED", logType="INFO")
        if autoStart:
            self.autoStart()

    def run(self):
        print("THE RUN METHOD")

    def autoStart(self):
        self.interface.log("Auto Start Enabled: Starting Node", logType='info')
        self._start()
        self._run()

    def _start_base(self):
        self._host._start()
        self.interface.log(f"{self.name} v{self.version} : HOST STARTED", logType="INFO")

    def _run_base(self):
        self.interface.log(f"{self.name} v{self.version} : RUN COMMANDED", logType="INFO")
        while True:
            start = time.time()
            self._run_error_handling()
            time.sleep(self._host.step_time - (start - time.time()))

    def _run_error_handling(self):
        try:
            self._host.step()
        except Exception as e:
            raise e


def handler(signal_received, frame):
    # Handle any cleanup here
    import TCS_interface
    interface = TCS_interface.interface("SYS")
    interface.log('SIGINT or CTRL-C detected. Exiting gracefully', 'EXIT MSG')
    sys.exit(0)


@atexit.register
def goodbye():
    import TCS_interface
    interface = TCS_interface.interface("SYS")
    interface.log('EXIT SEE ABOVE IF EXIT REASON IS KNOWN', 'EXIT MSG')


if __name__ == "__main__":
    # print license
    inter = TCS_interface.interface("SYS_LICENSE")
    inter.log_multiline(TCS_utils.LICENSE, "LICENSE")
    del inter

    signal(SIGINT, handler)
    argv = sys.argv
    if len(argv) > 1:
        nodename = argv[1]
    else:
        nodename = "N000"
    ran_instance = run(nodename)
    ran_instance._start()
    ran_instance._run()
else:
    signal(SIGINT, handler)
