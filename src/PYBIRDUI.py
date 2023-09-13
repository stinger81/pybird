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

import TCS_UIutils
import TCS_interface
import TCS_utils

export = TCS_interface.interface("EXPORT INTERFACE")
print(TCS_utils.LICENSE)



def _UI():
    ui = TCS_UIutils.userInterface("Main Menu", "PyBird UI (Run PYBIRDMgrUI.py to add keys/credentials)")
    ui.addOption("LOG COMMANDS", "")
    ui.addOption("ex", "Export Logs", export.export_log)
    ui.addOption("exc", "Export and Clear Logs", export.export_and_clear)
    ui.addQuit(isDefault=True)
    ui.run()


if __name__ == "__main__":
    _UI()
