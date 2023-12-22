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
    # region remove keys
    def remove_entire_app_keys_ui(self):
        # find all apps
        _app_path = TCS_variables.PYBIRD_HOME_APP_DIRECTORY
        _apps = os.listdir(_app_path)
        if len(_apps) == 0:
            self.interface.log("No apps found in " + _app_path, "ERROR")
            return
        appToRemove = TCS_utils.getUserInput_listChoice(in_prompt="Select App to remove",
                                                        in_options=_apps)

        # confirm removal
        confirm = TCS_utils.getUserInput_Confirm(in_prompt="Are you sure you want to remove " + appToRemove + " keys?",
                                                 in_confirmation_code="CONFIRM",
                                                 case_sensitive=True)

        if not confirm:
            self.interface.log("Removal of " + appToRemove + " cancelled")
            return
        else:
            self.interface.log("Removing " + appToRemove + " keys")
            _app_path = TCS_variables.PYBIRD_APP_HOME_DIR(appToRemove)
            # print(_app_path)
            shutil.rmtree(_app_path)
            self.interface.log("Removed " + appToRemove + " keys")

    def remove_specific_key_ui(self):
        # find all apps
        _app_path = TCS_variables.PYBIRD_HOME_APP_DIRECTORY
        _apps = os.listdir(_app_path)
        if len(_apps) == 0:
            self.interface.log("No apps found in " + _app_path, "ERROR")
            return
        app_to_remove_key_from = TCS_utils.getUserInput_listChoice(in_prompt="Select App to Remove Key From",
                                                                   in_options=_apps)

        # find all keys
        _app_key_path = TCS_variables.PYBIRD_APP_HOME_DIR(app_to_remove_key_from)
        _app_key_categories = os.listdir(_app_key_path)
        if len(_app_key_categories) == 0:
            self.interface.log("No keys found in " + _app_key_path, "ERROR")
            return
        key_cat_to_remove = TCS_utils.getUserInput_listChoice(in_prompt="Select Category",
                                                          in_options=_app_key_categories)
        key_cat_path = os.path.join(_app_key_path, key_cat_to_remove)
        _app_keys = os.listdir(key_cat_path)
        if len(_app_keys) == 0:
            self.interface.log("No keys found in " + key_cat_path, "ERROR")
            return
        key_to_remove = TCS_utils.getUserInput_listChoice(in_prompt="Select Key to Remove",
                                                          in_options=_app_keys)
        # confirm removal
        confirm = TCS_utils.getUserInput_Confirm(in_prompt="Are you sure you want to remove " + key_to_remove + " from " + app_to_remove_key_from + " keys?",
                                                    in_confirmation_code="CONFIRM",
                                                    case_sensitive=True)
        if confirm:
            self.interface.log("Removing " + key_to_remove + " from " + app_to_remove_key_from + " keys")
            key_path = os.path.join(key_cat_path, key_to_remove)
            os.remove(key_path)
            self.interface.log("Removed " + key_to_remove + " from " + app_to_remove_key_from + " keys")

    # endregion
    ################################################################################################
    ################################################################################################
    # region twitter_keys

    def _add_twitter_key(self, app_name):
        file = TCS_variables.PYBIRD_APP_X_KEY(app_name)

        keys = ""
        keys += self._keys[app_name]["api_key"]
        keys += "," +self._keys[app_name]["api_secret"]
        keys += "," + self._keys[app_name]["bearer_token"]
        keys += "," + self._keys[app_name]["access_token"]
        keys += "," + self._keys[app_name]["access_token_secret"]
        keys += "," + self._keys[app_name]["client_id"]
        keys += "," + self._keys[app_name]["client_secret"]

        self._save_key_to_file(file, keys)

        self.interface.dlog("Credentials for " + app_name + " added!")

    def load_twitter_keys(self, app_name)-> str:
        file = TCS_variables.PYBIRD_APP_X_KEY(app_name)
        self.interface.dlog("Twitter Creds File: " + file, "FILE LOC")
        return self._read_key_from_file(file).strip()


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
            file = TCS_variables.PYBIRD_APP_ATLAS_KEY(creds.app_name,creds.dedicated_name)

            keys = creds.app_name
            keys += "," + self._encode_key(creds.uri)
            keys += "," + self._encode_key(creds.api_version)
            keys += "," + self._encode_key(creds.dedicated_name)

            self._save_key_to_file(file, keys)

        if creds.shared:
            file = TCS_variables.PYBIRD_APP_ATLAS_KEY(creds.app_name,creds.shared_name)

            keys = creds.app_name
            keys += "," + self._encode_key(creds.uri)
            keys += "," + self._encode_key(creds.api_version)
            keys += "," + self._encode_key(creds.shared_name)

            self._save_key_to_file(file, keys)

    def load_atlas_keys(self,app_name, db_name) -> atlas_credentials_loaded:
        file = TCS_variables.PYBIRD_APP_ATLAS_KEY(app_name, db_name)
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
    # region General Keys

    def _add_general_key(self, appname: str, keyname: str, key: str):
        # directory = os.path.join(TCS_variables.PYBIRD_HOME_GENERAL_DIRECTORY, appname.upper())
        # if not os.path.exists(directory):
        #     os.mkdir(directory)
        # file = os.path.join(directory, str(keyname.upper() + ".key"))
        file = TCS_variables.PYBIRD_APP_GENERAL_KEY(appname, keyname)

        self.interface.dlog("General Key File " + str(tuple((appname, keyname))) + ": " + file, "FILE LOC")
        if os.path.exists(file):
            self.interface.dlog("Updating " + file + " credentials")
            TCS_utils.copy_file_to_old(file)
            TCS_utils.delete_file(file)

        key_encoded = self._encode_key(key)

        self._save_key_to_file(file, key_encoded)
        self.interface.dlog("Credentials for " + str(tuple((appname, keyname))) + " added!")

    def load_general_keys(self, appname: str, keyname: str):
        # file = os.path.join(TCS_variables.PYBIRD_HOME_GENERAL_DIRECTORY, appname.upper(), str(keyname.upper() + ".key"))
        file = TCS_variables.PYBIRD_APP_GENERAL_KEY(appname, keyname)

        self.interface.dlog("General Key File " + str(tuple((appname, keyname))) + ": " + file, "FILE LOC")
        if not os.path.exists(file):
            raise TCS_variables.PYBIRDAPPkeyERROR("Unable to find key file for " + str(tuple((appname, keyname))) + "!")
        else:
            key_encoded = self._read_key_from_file(file)
            return self._decode_key(key_encoded)

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

        key_encode = keys.encode(TCS_variables.AES_ENCODING)

        if self.config.encryption.encrypt_app_key:
            keys_enc = self.AES.encrypt(keys).decode(TCS_variables.AES_ENCODING)
            keys_enc_encode = keys_enc.encode(TCS_variables.AES_ENCODING)
            TCS_utils.append_text_file(file, keys_enc)
            TCS_utils.append_text_file(file, hashlib.sha256(keys_enc_encode).hexdigest())
            TCS_utils.append_text_file(file, hashlib.sha256(key_encode).hexdigest())
        else:
            TCS_utils.append_text_file(file, keys)
            TCS_utils.append_text_file(file, hashlib.sha256(key_encode).hexdigest())

    def _read_key_from_file(self, file: str):
        if not os.path.exists(file):
            self.interface.log("Unable to find key file for " + file + "!")
            return None

        with open(file, "r") as f:
            keys = f.readlines()
            key = keys[0].strip()
            save_hash = keys[1].strip()
            if hashlib.sha256(key.encode(TCS_variables.AES_ENCODING)).hexdigest() != save_hash:
                self.interface.log("File " + file + " is corrupted! FAILED INITIAL HASH CHECK ", "ERROR")
                return None
            if self.config.encryption.encrypt_app_key:
                decrypt_key_hash = keys[2].strip()
                key = self.AES.decrypt(key).decode(TCS_variables.AES_ENCODING)
                if hashlib.sha256(key.encode(TCS_variables.AES_ENCODING)).hexdigest() != decrypt_key_hash:
                    self.interface.log("File " + file + " is corrupted! FAILED SECOND HASH CHECK ", "ERROR")
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
            self.upload_generic_keys()
            if self.config.credentials.delete_dir_after_upload:
                self.interface.log(str("deleting directory: " + TCS_variables.PYBIRD_ADD_CRED_DIRECTORY))
                shutil.rmtree(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY)
        else:
            self.interface.log(str("directory does not exit to upload"))

    def upload_twitter_keys(self):
        for file in os.listdir(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY):
            if TCS_variables.EXT_UPLOAD_X in file:
                appName = file.replace(TCS_variables.EXT_UPLOAD_X, "")
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
            if TCS_variables.EXT_UPLOAD_ATLAS in file:
                appName = file.replace(TCS_variables.EXT_UPLOAD_ATLAS, "")
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

    def upload_generic_keys(self):
        for file in os.listdir(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY):
            if TCS_variables.EXT_UPLOAD_GENERAL in file:
                info = file.replace(TCS_variables.EXT_UPLOAD_GENERAL, "").split(".")
                appName = info[0].upper()
                keyname = info[1].upper()
                file_path = os.path.join(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY, file)
                with open(file_path, "r") as f:
                    new_cred = f.readline().strip()
                self._add_general_key(appName, keyname, new_cred)
                self.interface.log(str("Added generic credentials for " + str(info) + " from " + file))
                if self.config.credentials.delete_file_after_upload:
                    self.interface.log(str("deleting: " + file_path), "DELETING")
                    os.remove(file_path)

    # endregion
    ################################################################################################


if __name__ == "__main__":
    k = keychain()
    k.remove_specific_key_ui()
    # k.add_app_key_ui()
    # self.interface.log(k.load_twitter_keys("TEST"))
