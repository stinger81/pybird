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
import base64
import hashlib
import json
import os
import shutil

import TCS_config
import TCS_interface
import TCS_utils
import TCS_variables
import TKS_encryption


class keychain:
    def __init__(self) -> None:
        self.version = TCS_utils.version()

        self._keys: dict = dict()
        self.AES = TKS_encryption.AES()
        self.config = TCS_config.TCS_config()

        self.interface = TCS_interface.interface("keychain")

    ################################################################################################
    # region add UI
    def add_twitter_key_ui(self):
        """
        Add App keys to .twitter/.app
        """

        print("Add/Update Twitter Key")
        print("WARNING: Keys are stored in a scrambles format and can be decoded by anyone with this source code")
        print("App Information")
        app_name = str(input("Enter App Name: "))

        self._keys[app_name] = dict()
        print("Consumer Keys")
        self._keys[app_name]["api_key"] = input("Enter API key: ")
        self._keys[app_name]["api_secret"] = input("Enter API secret: ")
        print("authentication token")
        self._keys[app_name]["bearer_token"] = input("Enter Bearer Token: ")
        self._keys[app_name]["access_token"] = input("Enter Access Token: ")
        self._keys[app_name]["access_token_secret"] = input("Enter Access token secret: ")
        print("oAuth2")
        self._keys[app_name]["client_id"] = input("Enter client ID: ")
        self._keys[app_name]["client_secret"] = input("Enter Client Secret: ")

        self._add_twitter_key(app_name)

    def add_atlas_key_ui(self):
        """
        Add App keys to .twitter/.atlas
        """
        print("Add/Update Atlas Key")
        print("WARNING: Keys are stored in a scrambles format and can be decoded by anyone with this source code")
        print("App Information")

        info = self.atlas_credentials()

        info.app_name = str(input("Enter App Name: ")).upper()

        info.uri = str(input("Enter Atlas URI (Username/Password MUST be included): "))

        info.api_version = str(input("Enter Atlas API Version [1]: "))
        if info.api_version == "":
            info.api_version = "1"

        dedicated = str(input("Is this information for a dedicated database? (y/n)[n]: "))
        if dedicated.lower() == "":
            info.dedicated = False
        elif dedicated.lower() == "y":
            info.dedicated = True
            info.dedicated_name = str(input("Enter Dedicated Database Name: [" + info.app_name + "_DB]"))
            if info.dedicated_name == "":
                info.dedicated_name = info.app_name + "_DB"
        else:
            info.dedicated = False

        shared = str(input("Is this information for a shared database? (y/n)[n]: "))
        if shared.lower() == "":
            info.shared = False
        elif shared.lower() == "y":
            info.shared = True
            info.shared_name = str(input("Enter Shared Database Name [" + info.app_name + "_ShareDB]: "))
        else:
            info.shared = False

        self._add_atlas_key(info)

    # endregion 
    ################################################################################################

    ################################################################################################
    # region twitter_keys

    def _add_twitter_key(self, app_name):
        file = os.path.join(TCS_variables.PYBIRD_HOME_APP_DIRECTORY, str(app_name + ".key"))

        keys = app_name
        # api_key
        keys += "," + self._encode_key(self._keys[app_name]["api_key"])

        # api_secret
        keys += "," + self._encode_key(self._keys[app_name]["api_secret"])

        # bearer_token
        keys += "," + self._encode_key(self._keys[app_name]["bearer_token"])

        # access_token
        keys += "," + self._encode_key(self._keys[app_name]["access_token"])

        # access_token_secret
        keys += "," + self._encode_key(self._keys[app_name]["access_token_secret"])

        # client_id
        keys += "," + self._encode_key(self._keys[app_name]["client_id"])

        # client_secret
        keys += "," + self._encode_key(self._keys[app_name]["client_secret"])
        # self.interface.dlog(keys,"UnEncrypted")

        self._save_key_to_file(file, keys)

        self.interface.dlog("Credentials for " + app_name + " added!")

    def load_twitter_keys(self, app_name):
        file = os.path.join(TCS_variables.PYBIRD_HOME_APP_DIRECTORY, str(app_name + ".key"))
        keys: dict = dict()
        self.interface.dlog("Twitter Creds File: " + file, "FILE LOC")
        if not os.path.exists(file):
            raise TCS_variables.PYBIRDAPPkeyERROR("Unable to find key file for " + app_name + "!")
        else:
            k = self._read_key_from_file(file)
            keys["raw"] = k.strip().split(",")
            keys["api_key"] = self._decode_key(keys["raw"][1])
            keys["api_secret"] = self._decode_key(keys["raw"][2])
            keys["bearer_token"] = self._decode_key(keys["raw"][3])
            keys["access_token"] = self._decode_key(keys["raw"][4])
            keys["access_token_secret"] = self._decode_key(keys["raw"][5])
            keys["client_id"] = self._decode_key(keys["raw"][6])
            keys["client_secret"] = self._decode_key(keys["raw"][7])
            return keys

    # endregion
    ################################################################################################
    ################################################################################################
    # region mongodb credentials

    class atlas_credentials:
        def __init__(self):
            self.app_name = ""
            self.uri = ""
            self.api_version = ""
            self.dedicated = False
            self.dedicated_name = ""
            self.shared = False
            self.shared_name = ""

    class atlas_credentials_loaded:
        def __init__(self):
            self.app_name = ""
            self.uri = ""
            self.api_version = ""
            self.db_name = ""

    def _add_atlas_key(self, creds: atlas_credentials):
        if creds.dedicated:
            file = os.path.join(TCS_variables.PYBIRD_HOME_ATLAS_DIRECTORY, str(creds.dedicated_name + ".key"))

            keys = creds.app_name
            keys += "," + self._encode_key(creds.uri)
            keys += "," + self._encode_key(creds.api_version)
            keys += "," + self._encode_key(creds.dedicated_name)

            self._save_key_to_file(file, keys)

        if creds.shared:
            file = os.path.join(TCS_variables.PYBIRD_HOME_ATLAS_DIRECTORY, str(creds.shared_name + ".key"))

            keys = creds.app_name
            keys += "," + self._encode_key(creds.uri)
            keys += "," + self._encode_key(creds.api_version)
            keys += "," + self._encode_key(creds.shared_name)

            self._save_key_to_file(file, keys)

    def load_atlas_keys(self, db_name) -> atlas_credentials_loaded:
        file = os.path.join(TCS_variables.PYBIRD_HOME_ATLAS_DIRECTORY, str(db_name + ".key"))
        creds = self.atlas_credentials_loaded()
        self.interface.dlog("Atlas Creds File: " + file, "FILE LOC")
        if not os.path.exists(file):
            raise TCS_variables.PYBIRDAPPkeyERROR("Unable to find key file for " + db_name + "!")
        else:
            k = self._read_key_from_file(file)
            raw = k.strip().split(",")
            creds.app_name = raw[0]
            creds.uri = self._decode_key(raw[1])
            creds.api_version = self._decode_key(raw[2])
            creds.db_name = self._decode_key(raw[3])

        return creds

    # endregion
    ################################################################################################
    ################################################################################################
    # region encode/decode
    def _encode_key(self, key: str):
        _bytes = key.encode(TCS_variables.AES_ENCODING)
        _b64_bytes = base64.b64encode(_bytes)
        _b64 = _b64_bytes.decode(TCS_variables.AES_ENCODING)
        return _b64

    def _decode_key(self, key: str):
        _b64_bytes: bytes = key.encode(TCS_variables.AES_ENCODING)
        _bytes: bytes = base64.b64decode(_b64_bytes)
        str_key = _bytes.decode(TCS_variables.AES_ENCODING)
        return (str_key)

    # endregion
    ################################################################################################
    ################################################################################################
    # region file system
    def _save_key_to_file(self, file: str, keys: str):
        if os.path.exists(file):
            self.interface.dlog("Updating " + file + " credentials")
            TCS_utils.copy_file_to_old(file)
            TCS_utils.delete_file(file)

        if self.config.encryption.encrypt_app_key:
            keys_enc = self.AES.encrypt(keys).decode(TCS_variables.AES_ENCODING)
            TCS_utils.append_text_file(file, keys_enc)
            TCS_utils.append_text_file(file, hashlib.sha256(keys_enc).hexdigest())
            TCS_utils.append_text_file(file, hashlib.sha256(keys).hexdigest())
        else:
            TCS_utils.append_text_file(file, keys)
            TCS_utils.append_text_file(file, hashlib.sha256(keys).hexdigest())

    def _read_key_from_file(self, file: str):
        with open(file, "r") as f:
            keys = f.readlines()
            key = keys[0]
            save_hash = keys[1]
            if hashlib.sha256(key).hexdigest() != save_hash:
                return None
            if self.config.encryption.encrypt_app_key:
                decrypt_key_hash = keys[2]
                key = self.AES.decrypt(keys).decode(TCS_variables.AES_ENCODING)
                if hashlib.sha256(key).hexdigest() != decrypt_key_hash:
                    return None
        return key

    # endregion
    ################################################################################################
    ################################################################################################
    # region auto add creds
    def check_new_creds(self):
        if os.path.exists(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY):
            self.upload_twitter_keys()
            self.upload_atlas_keys()
            if self.config.credentials.delete_dir_after_upload:
                self.interface.log(str("deleting directory: " + TCS_variables.PYBIRD_ADD_CRED_DIRECTORY))
                shutil.rmtree(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY)
        else:
            self.interface.log(str("directory does not exit to upload"))

    def upload_twitter_keys(self):
        for file in os.listdir(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY):
            if ".x.json" in file:
                appName = file.replace(".x.json", "")
                file_path = os.path.join(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY, file)
                with open(file_path, "r") as f:
                    new_cred = json.load(f)
                try:
                    new_cred_base = new_cred[appName]
                except:
                    self.interface.log(str("APP NAME NOT VALID FOR FILE " + appName + " from " + file), logType='ERROR')
                    continue

                try:
                    self._keys[appName] = dict()
                    self._keys[appName]["api_key"] = new_cred_base["consumer_key"]["api_key"]
                    self._keys[appName]["api_secret"] = new_cred_base["consumer_key"]["api_secret"]
                    self._keys[appName]["bearer_token"] = new_cred_base["authentication_token"]["bearer_token"]
                    self._keys[appName]["access_token"] = new_cred_base["authentication_token"]["access_token"]
                    self._keys[appName]["access_token_secret"] = new_cred_base["authentication_token"][
                        "access_token_secret"]
                    self._keys[appName]["client_id"] = new_cred_base["oAuth2"]["client_id"]
                    self._keys[appName]["client_secret"] = new_cred_base["oAuth2"]["client_secret"]
                except:
                    self.interface.log(str("unable to read twitter credentials for " + appName + " from " + file),
                                       logType='ERROR')
                    continue

                self._add_twitter_key(app_name=appName)
                self.interface.log(str("Added twitter credentials for " + appName + " from " + file))

                if self.config.credentials.delete_file_after_upload:
                    self.interface.log(str("deleting: " + file_path), "DELETING")
                    os.remove(file_path)

    def upload_atlas_keys(self):
        for file in os.listdir(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY):
            if ".atlas.json" in file:
                appName = file.replace(".atlas.json", "")
                file_path = os.path.join(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY, file)
                with open(file_path, "r") as f:
                    new_cred = json.load(f)
                try:
                    new_cred_base = new_cred[appName]
                except:
                    self.interface.log(str("APP NAME NOT VALID FOR FILE " + appName + " from " + file), logType='ERROR')
                    continue
                try:
                    creds = self.atlas_credentials()
                    creds.app_name = appName
                    creds.uri = new_cred_base["uri"]
                    creds.api_version = new_cred_base["api_version"]
                    creds.dedicated = new_cred_base["dedicated"]["dedicated_allowed"]
                    creds.dedicated_name = new_cred_base["dedicated"]["dedicated_name"]
                    creds.shared = new_cred_base["shared"]["shared_allowed"]
                    creds.shared_name = new_cred_base["shared"]["shared_name"]
                except:
                    self.interface.log(str("unable to read atlas credentials for " + appName + " from " + file),
                                       logType='ERROR')
                    continue

                self._add_atlas_key(creds)
                self.interface.log(str("Added atlas credentials for " + appName + " from " + file))

                if self.config.credentials.delete_file_after_upload:
                    self.interface.log(str("deleting: " + file_path), "DELETING")
                    os.remove(file_path)

    # endregion
    ################################################################################################


if __name__ == "__main__":
    k = keychain()
    # k.add_app_key_ui()
    # self.interface.log(k.load_twitter_keys("TEST"))
