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
import base64
import hashlib
import json
import os
import shutil
from typing import Union

import TCS_config
import TCS_interface
import TCS_utils
import TCS_variables
import TKS_encryption


class keychain:
    def __init__(self) -> None:
        self.version = TCS_utils.version()

        # self._keys: dict = dict()
        self.AES = TKS_encryption.AES()
        self.config = TCS_config.TCS_config()

        self.interface = TCS_interface.interface("keychain")


    ################################################################################################
    # region add UI
    def add_twitter_key_ui(self)->None:
        """
        Add twitter keys to apps twitter key directory
        :return:
        """

        print("Add/Update Twitter Key")
        print("WARNING: Keys are stored in a scrambles format and can be decoded by anyone with this source code")
        print("App Information")

        app_name = TCS_utils.getUserInput_required_minimum_length(in_prompt="Enter App Name", in_length=4)
        api_key = TCS_utils.getUserInput(in_prompt="Enter API key", in_default="")
        api_secret = TCS_utils.getUserInput(in_prompt="Enter API secret", in_default="")
        bearer_token = TCS_utils.getUserInput(in_prompt="Enter Bearer Token", in_default="")
        access_token = TCS_utils.getUserInput(in_prompt="Enter Access Token", in_default="")
        access_token_secret = TCS_utils.getUserInput(in_prompt="Enter Access token secret", in_default="")
        client_id = TCS_utils.getUserInput(in_prompt="Enter client ID", in_default="")
        client_secret = TCS_utils.getUserInput(in_prompt="Enter Client Secret", in_default="")

        if TCS_utils.getUserInput_Confirm(in_prompt="Do you want to save this key?",
                                          in_confirmation_code="CONFIRM",
                                          in_case_sensitive=True):
            self.interface.log("Saving Key")
            self._add_twitter_key(in_app_name=app_name,
                                  in_api_key=api_key,
                                  in_api_secret=api_secret,
                                  in_bearer_token=bearer_token,
                                  in_access_token=access_token,
                                  in_access_token_secret=access_token_secret,
                                  in_client_id=client_id,
                                  in_client_secret=client_secret)
        else:
            self.interface.log("Key not saved")

        # app_name = str(input("Enter App Name: "))
        #
        # _keys = dict()
        # _keys[app_name] = dict()
        # print("Consumer Keys")
        # _keys[app_name]["api_key"] = input("Enter API key: ")
        # _keys[app_name]["api_secret"] = input("Enter API secret: ")
        # print("authentication token")
        # _keys[app_name]["bearer_token"] = input("Enter Bearer Token: ")
        # _keys[app_name]["access_token"] = input("Enter Access Token: ")
        # _keys[app_name]["access_token_secret"] = input("Enter Access token secret: ")
        # print("oAuth2")
        # _keys[app_name]["client_id"] = input("Enter client ID: ")
        # _keys[app_name]["client_secret"] = input("Enter Client Secret: ")
        #
        # self._add_twitter_key(app_name, in_keys=_keys)

    def add_atlas_key_ui(self)->None:
        """
        add atlas keys to apps atlas key directory
        :return:
        """
        print("Add/Update Atlas Key")
        print("WARNING: Keys are stored in a scrambles format and can be decoded by anyone with this source code")
        print("App Information")

        app_name = TCS_utils.getUserInput_required_minimum_length(in_prompt="Enter App Name", in_length=4)
        uri = TCS_utils.getUserInput(in_prompt="Enter Atlas URI (Username/Password MUST be included)",in_default="")
        api_version = TCS_utils.getUserInput_int(in_prompt="Enter Atlas API Version ",in_default=1)
        db_name = TCS_utils.getUserInput(in_prompt="Enter Database Name: ",in_default="")

        if TCS_utils.getUserInput_Confirm(in_prompt="Do you want to save this key?",
                                          in_confirmation_code="CONFIRM",
                                          in_case_sensitive=True):
            self.interface.log("Saving Key")
            self._add_atlas_key(in_appname=app_name,
                                in_uri=uri,
                                in_api_version=api_version,
                                in_db_name=db_name)
        else:
            self.interface.log("Key not saved")

        # self._add_atlas_key(in_appname=app_name,
        #                     in_uri=uri,
        #                     in_api_version=api_version,
        #                     in_db_name=db_name)

        # info = self.atlas_credentials()
        #
        # info.app_name = str(input("Enter App Name: ")).upper()
        #
        # info.uri = str(input("Enter Atlas URI (Username/Password MUST be included): "))
        #
        # info.api_version = str(input("Enter Atlas API Version [1]: "))
        # if info.api_version == "":
        #     info.api_version = "1"
        #
        # dedicated = str(input("Is this information for a dedicated database? (y/n)[n]: "))
        # if dedicated.lower() == "":
        #     info.dedicated = False
        # elif dedicated.lower() == "y":
        #     info.dedicated = True
        #     info.dedicated_name = str(input("Enter Dedicated Database Name: [" + info.app_name + "_DB]"))
        #     if info.dedicated_name == "":
        #         info.dedicated_name = info.app_name + "_DB"
        # else:
        #     info.dedicated = False
        #
        # shared = str(input("Is this information for a shared database? (y/n)[n]: "))
        # if shared.lower() == "":
        #     info.shared = False
        # elif shared.lower() == "y":
        #     info.shared = True
        #     info.shared_name = str(input("Enter Shared Database Name [" + info.app_name + "_ShareDB]: "))
        # else:
        #     info.shared = False
        #
        # self._add_atlas_key(info)

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
                                                 in_case_sensitive=True)

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
        confirm = TCS_utils.getUserInput_Confirm(
            in_prompt="Are you sure you want to remove " + key_to_remove + " from " + app_to_remove_key_from + " keys?",
            in_confirmation_code="CONFIRM",
            in_case_sensitive=True)
        if confirm:
            self.interface.log("Removing " + key_to_remove + " from " + app_to_remove_key_from + " keys")
            key_path = os.path.join(key_cat_path, key_to_remove)
            os.remove(key_path)
            self.interface.log("Removed " + key_to_remove + " from " + app_to_remove_key_from + " keys")

    # endregion
    ################################################################################################
    ################################################################################################
    # region twitter_keys

    def _add_twitter_key(self,
                         in_app_name: str,
                         in_api_key: str,
                         in_api_secret: str,
                         in_bearer_token: str,
                         in_access_token: str,
                         in_access_token_secret: str,
                         in_client_id: str,
                         in_client_secret: str
                         ) -> None:
        """
        Add App keys to the apps twitter key directory
        :param in_app_name:
        :param in_api_key:
        :param in_api_secret:
        :param in_bearer_token:
        :param in_access_token:
        :param in_access_token_secret:
        :param in_client_id:
        :param in_client_secret:
        :return:
        """
        my_save_file = TCS_variables.PYBIRD_APP_X_KEY(in_app_name)
        keys = ",".join([in_api_key,
                         in_api_secret,
                         in_bearer_token,
                         in_access_token,
                         in_access_token_secret,
                         in_client_id,
                         in_client_secret])
        self._save_key_to_file(my_save_file, keys)
        self.interface.dlog("Credentials for " + in_app_name + " added!")

    # def _add_twitter_key(self, in_app_name: str, in_keys: dict):
    #     file = TCS_variables.PYBIRD_APP_X_KEY(in_app_name)
    #
    #     keys = ""
    #     keys += in_keys[in_app_name]["api_key"]
    #     keys += "," + in_keys[in_app_name]["api_secret"]
    #     keys += "," + in_keys[in_app_name]["bearer_token"]
    #     keys += "," + in_keys[in_app_name]["access_token"]
    #     keys += "," + in_keys[in_app_name]["access_token_secret"]
    #     keys += "," + in_keys[in_app_name]["client_id"]
    #     keys += "," + in_keys[in_app_name]["client_secret"]
    #
    #     self._save_key_to_file(file, keys)
    #
    #     self.interface.dlog("Credentials for " + in_app_name + " added!")

    def load_twitter_keys(self, in_app_name) -> list:
        """
        Load App keys from the apps twitter key directory
        :param in_app_name:
        :return: list of keys
        [api_key, api_secret, bearer_token, access_token, access_token_secret, client_id, client_secret]
        """
        file = TCS_variables.PYBIRD_APP_X_KEY(in_app_name)
        self.interface.dlog("Twitter Creds File: " + file, "FILE LOC")
        return self._read_key_from_file(file).strip().split(",")

    # endregion
    ################################################################################################
    ################################################################################################
    # region mongodb credentials

    # class atlas_credentials:
    #     def __init__(self):
    #         self.app_name = ""
    #         self.uri = ""
    #         self.api_version = ""
    #         self.dedicated = False
    #         self.dedicated_name = ""
    #         self.shared = False
    #         self.shared_name = ""

    # class atlas_credentials_loaded:
    #     def __init__(self):
    #         self.app_name = ""
    #         self.uri = ""
    #         self.api_version = ""
    #         self.db_name = ""

    def _add_atlas_key(self,
                       in_appname: str,
                       in_uri: str,
                       in_api_version: Union[int, str],
                       in_db_name: str
                       ) -> None:
        """
        Add App keys to the apps atlas key directory
        :param in_appname:
        :param in_uri:
        :param in_api_version:
        :param in_db_name:
        :return:
        """
        my_save_file = TCS_variables.PYBIRD_APP_ATLAS_KEY(in_appname, in_db_name)

        keys = ",".join([in_appname, in_uri, in_api_version, in_db_name])
        # keys += in_appname
        # keys += "," + in_uri
        # keys += "," + in_api_version
        # keys += "," + in_db_name

        self._save_key_to_file(my_save_file, keys)
        self.interface.dlog("Credentials for atlas " + in_appname + " added!")
        # if creds.dedicated:
        #     file = TCS_variables.PYBIRD_APP_ATLAS_KEY(creds.app_name, creds.dedicated_name)
        #
        #     keys = creds.app_name
        #     keys += "," + creds.uri
        #     keys += "," + creds.api_version
        #     keys += "," + creds.dedicated_name
        #
        #     self._save_key_to_file(file, keys)
        #
        # if creds.shared:
        #     file = TCS_variables.PYBIRD_APP_ATLAS_KEY(creds.app_name, creds.shared_name)
        #
        #     keys = creds.app_name
        #     keys += "," + creds.uri
        #     keys += "," + creds.api_version
        #     keys += "," + creds.shared_name
        #
        #     self._save_key_to_file(file, keys)

    def load_atlas_keys(self, app_name: str, db_name: str) -> list:
        """
        Load App keys from the apps atlas key directory
        :param app_name: app name
        :param db_name: database name
        :return: list of parameters
        [appname, uri, api_version, db_name]
        """
        file = TCS_variables.PYBIRD_APP_ATLAS_KEY(app_name, db_name)
        # creds = self.atlas_credentials_loaded()
        self.interface.dlog("Atlas Creds File: " + file, "FILE LOC")
        # if not os.path.exists(file):
        #     raise TCS_variables.PYBIRDAPPkeyERROR("Unable to find key file for " + db_name + "!")
        # else:
        #     k = self._read_key_from_file(file)
        #     raw = k.strip().split(",")
        #     # creds.app_name = raw[0]
        #     # creds.uri = self._decode_key(raw[1])
        #     # creds.api_version = self._decode_key(raw[2])
        #     # creds.db_name = self._decode_key(raw[3])
        #     return raw
        return self._read_key_from_file(file).strip().split(",")

    # endregion
    ################################################################################################
    ################################################################################################
    # region General Keys

    def _add_general_key(self, appname: str, keyname: str, key: str):
        """
        Add App keys to the apps general key directory
        :param appname:
        :param keyname:
        :param key:
        :return:
        """

        file = TCS_variables.PYBIRD_APP_GENERAL_KEY(appname, keyname)

        self.interface.dlog("General Key File " + str(tuple((appname, keyname))) + ": " + file, "FILE LOC")
        if os.path.exists(file):
            self.interface.dlog("Updating " + file + " credentials")
            TCS_utils.copy_file_to_old(file)
            TCS_utils.delete_file(file)

        key_encoded = self._encode_key(key)

        self._save_key_to_file(file, key_encoded)
        self.interface.dlog("Credentials for " + str(tuple((appname, keyname))) + " added!")

    def load_general_keys(self, appname: str, keyname: str) -> str:
        """
        Load App keys from the apps general key directory
        :param appname:
        :param keyname:
        :return:
        """
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
    def _encode_key(self, key: str) -> str:
        """
        :param key: standard string key
        :return: base64 encoded key
        """
        _bytes = key.encode(TCS_variables.AES_ENCODING)
        _b64_bytes = base64.b64encode(_bytes)
        _b64 = _b64_bytes.decode(TCS_variables.AES_ENCODING)
        return _b64

    def _decode_key(self, key: str) -> str:
        """
        :param key: base 64 encoded key
        :return: standard string key
        """
        _b64_bytes: bytes = key.encode(TCS_variables.AES_ENCODING)
        _bytes: bytes = base64.b64decode(_b64_bytes)
        str_key = _bytes.decode(TCS_variables.AES_ENCODING)
        return str_key

    # endregion
    ################################################################################################
    ################################################################################################
    # region file system
    def _save_key_to_file(self, file: str, keys: str):
        """
        Save keys to file
        :param file:
        :param keys:
        :return:
        """
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

    def _read_key_from_file(self, file: str) -> Union[str, None]:
        """
        Read key from file
        :param file: file name
        :return: returns the keys if valid, None if invalid
        """
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
    def check_new_creds(self) -> None:
        """
        Check for new credentials to add
        Checks for credentials in the $PYBIRD/add_cred
            - twitter credentials '.x.json'
                - EX: 'myapp.x.json'
            - atlas credentials '.atlas.json'
                - EX: 'myapp.atlas.json'
            - general credentials '.gen.txt'
                - EX: 'myapp.mykey.gen.txt'

        :return:
        """
        if os.path.exists(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY):
            self.upload_twitter_keys()
            self.upload_atlas_keys()
            self.upload_generic_keys()
            if self.config.credentials.delete_dir_after_upload:
                self.interface.log(str("deleting directory: " + TCS_variables.PYBIRD_ADD_CRED_DIRECTORY))
                shutil.rmtree(TCS_variables.PYBIRD_ADD_CRED_DIRECTORY)
        else:
            self.interface.log(str("directory does not exit to upload"))

    def upload_twitter_keys(self) -> None:
        """
        Checks for credentials in the $PYBIRD/add_cred
            - twitter credentials '.x.json'
                - EX: 'myapp.x.json'
        :return:
        """
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
                    consumer_key = new_cred_base["consumer_key"]
                    authentication_token = new_cred_base["authentication_token"]
                    oAuth2 = new_cred_base["oAuth2"]
                except:
                    self.interface.log(str("unable to read twitter credentials for " + appName + " from " + file),
                                       logType='ERROR')
                    continue

                self._add_twitter_key(in_app_name=appName,
                                      in_api_key=consumer_key["api_key"],
                                      in_api_secret=consumer_key["api_secret"],
                                      in_bearer_token=authentication_token["bearer_token"],
                                      in_access_token=authentication_token["access_token"],
                                      in_access_token_secret=authentication_token["access_token_secret"],
                                      in_client_id=oAuth2["client_id"],
                                      in_client_secret=oAuth2["client_secret"]
                                      )

                self.interface.log(str("Added twitter credentials for " + appName + " from " + file))

                # try:
                #     _keys = dict()
                #     _keys[appName] = dict()
                #     _keys[appName]["api_key"] = new_cred_base["consumer_key"]["api_key"]
                #     _keys[appName]["api_secret"] = new_cred_base["consumer_key"]["api_secret"]
                #     _keys[appName]["bearer_token"] = new_cred_base["authentication_token"]["bearer_token"]
                #     _keys[appName]["access_token"] = new_cred_base["authentication_token"]["access_token"]
                #     _keys[appName]["access_token_secret"] = new_cred_base["authentication_token"]["access_token_secret"]
                #     _keys[appName]["client_id"] = new_cred_base["oAuth2"]["client_id"]
                #     _keys[appName]["client_secret"] = new_cred_base["oAuth2"]["client_secret"]
                # except:
                #     self.interface.log(str("unable to read twitter credentials for " + appName + " from " + file),
                #                        logType='ERROR')
                #     continue
                #
                # self._add_twitter_key(in_app_name=appName, keys=_keys)
                # self.interface.log(str("Added twitter credentials for " + appName + " from " + file))

                if self.config.credentials.delete_file_after_upload:
                    self.interface.log(str("deleting: " + file_path), "DELETING")
                    os.remove(file_path)

    def upload_atlas_keys(self):
        """
        Checks for credentials in the $PYBIRD/add_cred
            - atlas credentials '.atlas.json'
                - EX: 'myapp.atlas.json'
        :return:
        """
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
                for cred in new_cred_base:
                    try:
                        self._add_atlas_key(in_appname=appName,
                                            in_uri=cred["uri"],
                                            in_api_version=cred["api_version"],
                                            in_db_name=cred["database_name"]
                                            )
                        self.interface.log(str("Added atlas credentials for " + appName + " from " + file))
                    except:
                        self.interface.log(str("unable to read atlas credentials for " + appName + " from " + file),
                                           logType='ERROR')
                        continue

                # try:
                #     creds = self.atlas_credentials()
                #     creds.app_name = appName
                #     creds.uri = new_cred_base["uri"]
                #     creds.api_version = new_cred_base["api_version"]
                #     creds.dedicated = new_cred_base["dedicated"]["dedicated_allowed"]
                #     creds.dedicated_name = new_cred_base["dedicated"]["dedicated_name"]
                #     creds.shared = new_cred_base["shared"]["shared_allowed"]
                #     creds.shared_name = new_cred_base["shared"]["shared_name"]
                # except:
                #     self.interface.log(str("unable to read atlas credentials for " + appName + " from " + file),
                #                        logType='ERROR')
                #     continue
                #
                # self._add_atlas_key(creds)
                # self.interface.log(str("Added atlas credentials for " + appName + " from " + file))

                if self.config.credentials.delete_file_after_upload:
                    self.interface.log(str("deleting: " + file_path), "DELETING")
                    os.remove(file_path)

    def upload_generic_keys(self):
        """
        Checks for credentials in the $PYBIRD/add_cred
            - general credentials '.gen.txt'
                - EX: 'myapp.mykey.gen.txt'
        :return:
        """
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
