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
import TCS_utils
import TCS_variables
import TKS_encryption
import TKS_keychain

print(TCS_utils.LICENSE)


def _UI():
    if TCS_variables.NETWORK_NAME != "":
        print("PYBIRD Mgr UI")
        print("WARNING: This manager will modify the local network setting listed below")
        print("WARNING: Please make sure this is the correct network")

        print("Network: " + TCS_variables.NETWORK_NAME)

        print("WARNING: This manager will modify the local network setting listed above")
        print("WARNING: If this is not the correct network, please exit now")

        user = TCS_utils.getUserInput_yn("Is '" + TCS_variables.NETWORK_NAME + "'  the correct network? ")

        if not user:
            print("Exiting")
            exit(0)

    aes_keychain = TKS_encryption._AES_keychain()

    ui = TCS_UIutils.userInterface("Main Menu", "Command in the UI are NOT Reversible")
    ui.addHeader("KEYCHAIN COMMANDS")
    ui.addOption("aes", "Add/Update AES-256 Key", aes_keychain._ui)

    try:
        keys = TKS_keychain.keychain()

        ui.addOption("app", "Add/Update App Key", keys.add_twitter_key_ui)
        ui.addOption("atlas", "Add/Update MongoDB Atlas Credentials", keys.add_atlas_key_ui)
        ui.addOption("upload", "Upload credentials in " + TCS_variables.PYBIRD_DIRECTORIES.ADD_CRED,
                     keys.check_new_creds,
                     requireConfirmation=True)
        ui.addOption("rmapp", "Remove App Key", keys.remove_entire_app_keys_ui)
        ui.addOption("rmsk", "Remove Specific Key from App", keys.remove_specific_key_ui)
    except:
        ui.addHeader("Encryption Enabled Must Add AES Key First, Before Adding Other Keys")

    ui.addHeader("VIEW COMMANDS")

    ui.addOption("vk", "view keychain directory structure, NO KEYS SHOWN", TCS_utils.pybird_keychain_tree)
    ui.addOption("vd", "view data directory structure", TCS_utils.pybird_data_tree)
    ui.addQuit(isDefault=True)
    while True:
        userChoice = ui.getUserResponse()
        method = userChoice[2]
        method()


if __name__ == "__main__":
    _UI()
