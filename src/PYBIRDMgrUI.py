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
    keys = TKS_keychain.keychain()
    aes_keychain = TKS_encryption._AES_keychain()
    atlas_creds = TKS_keychain.keychain()

    ui = TCS_UIutils.userInterface("Main Menu", "Command in the UI are NOT Reversible")
    ui.addOption("aes", "Add/Update AES-256 Key", aes_keychain._ui)
    ui.addOption("app", "Add/Update App Key", keys.add_twitter_key_ui)
    ui.addOption("atlas", "Add/Update MongoDB Atlas Credentials", atlas_creds.add_atlas_key_ui)
    ui.addOption("upload", "Upload credentials in " + TCS_variables.PYBIRD_ADD_CRED_DIRECTORY, keys.check_new_creds,
                 requireConfirmation=True)
    ui.addOption("rmapp", "Remove App Key", keys.remove_entire_app_keys_ui)
    ui.addOption("rmsk", "Remove Specific Key from App", keys.remove_specific_key_ui)
    ui.addQuit(isDefault=True)
    while True:
        userChoice = ui.getUserResponse()
        method = userChoice[2]
        method()


if __name__ == "__main__":
    _UI()
