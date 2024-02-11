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


import TCS_UIutils
import TCS_interface
import TCS_utils

export = TCS_interface.interface("EXPORT INTERFACE", pybird_app=True)
print(TCS_utils.LICENSE)


def _UI():
    ui = TCS_UIutils.userInterface("Main Menu", "PyBird UI (Run PYBIRDMgrUI.py to add keys/credentials)")
    ui.addHeader("EXPORT ALL LOGS")
    ui.addOption("ex", "Export ALL Logs", export.export_log)
    ui.addOption("exm", "Export ALL Master Logs", export.export_master_log)
    ui.addOption("exs", "Export ALL Session Logs", export.export_session_log)
    ui.addOption("exa", "Export ALL App Logs ", export.export_app_log)
    ui.addOption("exsa", "Export ALL Pybird System App Logs", export.export_sysapp_log)

    ui.addHeader("EXPORT SPECIFIC LOGS")
    ui.addOption("ess", "Export Specific Session Logs", export.export_session_log_select)
    ui.addOption("esa", "Export Specific App Logs", export.export_app_log_select)
    ui.addOption("essa", "Export Specific Pybird System App Logs", export.export_sysapp_log_select)



    ui.addHeader("BUILD LOGS")
    ui.addOption("bm", "Build Master Log From Session Logs", export.build_master_from_session_logs)

    ui.addHeader("CLEAR LOGS")
    ui.addOption("exc", "Export and Clear Logs", export.export_and_clear, requireConfirmation=True)

    ui.addQuit(isDefault=True)
    ui.run()


if __name__ == "__main__":
    _UI()
