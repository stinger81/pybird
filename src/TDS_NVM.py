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
import sys

import TCS_interface
import TCS_variables
import TKS_encryption


class NVM_dataInterface:
    def __init__(self, app_code: str, save_key: str = "") -> None:
        self._app_code = app_code
        self._save_key = save_key
        if save_key == "":
            self._encryption = False
        else:
            self._encryption = True
            self._my_aes = TKS_encryption.AES_savekey(app_name=self._app_code, save_key=self._save_key)
        self._app_dir = os.path.join(TCS_variables.PYBIRD_DIRECTORIES.DATA_APPDATA, app_code.upper())
        if not os.path.exists(self._app_dir):
            os.makedirs(self._app_dir)

    def _file_name(self, data_name: str):
        filename = ""
        filename += str(self._app_code)
        filename += "__"
        filename += data_name.replace(" ", "_")
        filename = filename.upper()
        filename += ".pkl"

        return os.path.join(self._app_dir, filename)

    def _file_enc_name(self, data_name: str):
        return self._file_name(data_name) + ".enc"

    def _get_file_name(self, data_name: str):
        if self._encryption:
            return self._file_enc_name(data_name)
        else:
            return self._file_name(data_name)

    def save(self, data_name: str, data):
        """
        Save data to file
        :param data_name:
        :param data:
        :return:
        """
        file = self._get_file_name(data_name)
        with open(file, 'wb') as f:
            my_data = pickle.dumps(data)
            if self._encryption:
                my_data_hex = my_data.hex()
                my_data_enc = self._my_aes.encrypt(my_data_hex)
                f.write(my_data_enc)
            else:
                f.write(my_data)

    def load(self, data_name: str):
        """
        Load data from file
        :param data_name:
        :return:
        """
        file = self._get_file_name(data_name)
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                if self._encryption:
                    try:
                        my_data_enc = f.read()
                        my_data_hex = self._my_aes.decrypt(my_data_enc.decode()).decode(TCS_variables.AES.ENCODING)
                        my_data = bytes.fromhex(my_data_hex)
                        return pickle.loads(bytes(my_data))
                    except EOFError as e:
                        app_inter = TCS_interface.interface(self._app_code)
                        app_inter.log("Error loading data: " + data_name, "ERROR")
                        app_inter.log("File may be corrupted or the save key may have changed", "ERROR")
                        del app_inter
                        if TCS_variables.SYS_ARG.RAISE[0] in sys.argv:
                            raise e

                        return None

                else:
                    try:
                        my_data = f.read()
                        return pickle.loads(my_data)
                    except EOFError as e:
                        app_inter = TCS_interface.interface(self._app_code)
                        app_inter.log("Error loading data: " + data_name, "ERROR")
                        app_inter.log("File may be corrupted", "ERROR")
                        del app_inter
                        if TCS_variables.SYS_ARG.RAISE[0] in sys.argv:
                            raise e

                        return None
        else:
            return None


if __name__ == "__main__":
    # app = "new"
    # name = "1"
    # DI = NVM_data(app_code=app, save_key="TEST!@#", data_name=name)
    #
    #
    # DI.data = ["test"]
    # for i in range(1000):
    #     DI.data.append(str(i)+"test")
    #
    # print(DI.data)
    # DI.save()
    # DI.load()
    # print(DI.data)
    # di = data_interface("new", "TEST!@#")
    # di.save_data("test", "test")
    # print(di.load_data("test"))
    di = NVM_dataInterface("new", "TEST!@#")
    di.save("test", "test")
    print(di.load("test"))
