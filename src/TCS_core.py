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

import TCS_config
import TCS_interface
import TCS_utils


class core:
    def __init__(self) -> None:
        # Description
        self.name = "TWcore"
        self.version = TCS_utils.version()

        self.description = "Core class for TWapp,TWnode, TWserver"

        # step info
        self.step_count = 0

        self.test = False  # used for testing code

        self.isApp = False

        self._config = TCS_config.TCS_config()

        # Interface
        self.interface = TCS_interface.interface("CORE")
        self.interface.dlog(
            f"{self.name} v{self.version} : CORE-BASE INITIALIZED", logType="INFO")

    ################################################################################

    def _settings(self):
        self.interface.update_dir()
        self._settings_base()
        self.mySettings()
        self.interface.dlog(
            f"{self.name} v{self.version} : SETTING CONFIGURED ", logType="INFO")

    def _settings_base(self):
        """
        Must be overridden in base app class
        """
        pass

    def mySettings(self):
        """
        Override this function to add your own settings
        """
        pass

    ##############################################################################
    # Operations Region

    def _start(self):
        # host will call on bootup
        self._start_base()
        self.myStart()
        self.interface.dlog(
            f"{self.name} v{self.version} : RUN COMMAND COMPLETE", logType="INFO")

        self._settings()

    def _start_base(self):
        """
        Must be overridden in base app class
        """
        pass

    def myStart(self):
        """
        Override this function to add your own init
        """
        pass

    def _run(self):
        self._run_base()
        self.myRun()

    def _run_base(self):
        """
        Must be overridden in base app class
        """
        pass

    def myRun(self):
        """
        Override this function to add your own run
        """
        pass

    def _pause(self):
        """
        Placeholder for future functionality
        """
        pass

    def _halt(self):
        """
        Placeholder for future functionality
        """
        pass

    def _request_reboot(self):
        """
        Placeholder for future functionality
        """
        pass

    def _handel_shutdown(self):
        self.myShutdown()
        """
        Placeholder for future functionality
        """
        pass

    def myShutdown(self):
        """
        Override this function to add your own shutdown
        """
        pass

    def _handle_cleanup(self):
        """
        Placeholder for future functionality
        """
        pass

    # End Region
    ##############################################################################

    ##############################################################################
    # Step Region
    def preStep(self):
        pass
    def step(self):
        self.step_count += 1
        self.preStep()
        self._step_base()
        self.myStep()
        self.postStep()

    def _step_base(self):
        """
        Must be overridden in base app class
        """
        pass

    def myStep(self):
        """
        Override this function to add your own step
        """
        pass
    def postStep(self):
        pass
    # End Region
    ##############################################################################
