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

import os
import pickle
import hashlib

import TCS_variables
import TCS_utils
import TKS_encryption



class data_interface:
    def __init__(self, app_code: str, save_key : str) -> None:
        self.app_code = app_code

        self.save_key = save_key

        self._app_dir = os.path.join(TCS_variables.PYBIRD_DIRECTORIES.DATA_APPDATA, app_code.upper())
        if not os.path.exists(self._app_dir):
            os.makedirs(self._app_dir)

    def save_data(self, data_name: str, data):
        _nvm = NVM_data(self.app_code, data_name=data_name, save_key=self.save_key)
        _nvm._init_write_only(data)
    def load_data(self, data_name):
        temp = NVM_data(self.app_code, data_name, save_key=self.save_key)
        temp._init_read_only()
        return temp.data

    def live_data(self, data_name: str):
        temp = NVM_data(self.app_code, data_name, save_key=self.save_key)
        temp._init_live()
        return temp


class NVM_data:
    def __init__(self, app_code: str, data_name: str, save_key:str) -> None:
        self._app_code = app_code
        self._data_name = data_name
        self._save_key = save_key
        self.data = None
        self._app_dir = os.path.join(TCS_variables.PYBIRD_DIRECTORIES.DATA_APPDATA, app_code.upper())

        if not os.path.exists(self._app_dir):
            os.makedirs(self._app_dir)

        fileName = ""
        fileName += str(self._app_code)
        fileName += "__"
        fileName += data_name
        fileName = fileName.upper()
        fileName += ".pkl"

        self._file = os.path.join(self._app_dir, fileName)
        self._file_enc = self.file_enc_name(self._file)

        self._my_aes = TKS_encryption.AES_savekey(app_name=self._app_code, save_key=self._save_key)

    def _init_read_only(self):
        if os.path.isfile(self._file):
            self.load()
        return self.data

    def _init_write_only(self, data):
        self.data = data
        self.close()

    def _init_live(self):
        if os.path.isfile(self._file):
            self.load()
        else:
            self.save()

    def __del__(self):
        pass

    def load(self):
        """
        reloads data
        :return:
        """
        with open(self._file_enc, 'r') as f:
            my_data_enc = f.read()
            my_data_hex = self._my_aes.decrypt(my_data_enc).decode(TCS_variables.AES.ENCODING)
            my_data = bytes.fromhex(my_data_hex)
            self.data = pickle.loads(bytes(my_data))


    def save(self):
        """
        saves the data
        :return:
        """
        with open(self._file_enc, 'w') as f:
            my_data = pickle.dumps(self.data)
            my_data_hex = my_data.hex()
            my_data_enc = self._my_aes.encrypt(my_data_hex).decode(TCS_variables.AES.ENCODING)
            f.write(my_data_enc)

    def update(self):
        self.load()

    def close(self):
        """
        saves and deletes self
        :return:
        """
        self.save()
        del self

    def file_enc_name(self, file_name):
        return self._file + ".enc"


if __name__ == "__main__":
    app = "new"
    name = "1"
    DI = NVM_data(app_code=app, save_key="TEST!@#", data_name=name)


    DI.data = ["test"]
    for i in range(1000):
        DI.data.append(str(i)+"test")

    print(DI.data)
    DI.save()
    DI.load()
    print(DI.data)
