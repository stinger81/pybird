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

import TCS_variables


class data_interface:
    def __init__(self, app_code: str) -> None:
        self.app_code = app_code
        self._app_dir = os.path.join(TCS_variables.PYBIRD_DATA_APPDATA_DIRECTORY, app_code.upper())
        if not os.path.exists(self._app_dir):
            os.makedirs(self._app_dir)

    def save_data(self, data_name: str, data):
        _nvm = NVM_data(self.app_code, data_name=data_name)
        _nvm._init_write_only(data)

    def load_data(self, data_name):
        temp = NVM_data(self.app_code, data_name, readOnly=True)
        temp._init_read_only()
        return temp.data

    def live_data(self, data_name: str):
        temp = NVM_data(self.app_code, data_name)
        temp._init_live()
        return temp


class NVM_data:
    def __init__(self, app_code: str, data_name: str) -> None:
        self._app_code = app_code
        self._data_name = data_name
        self.data = None
        self._app_dir = os.path.join(TCS_variables.PYBIRD_DATA_APPDATA_DIRECTORY, app_code.upper())

        if not os.path.exists(self._app_dir):
            os.makedirs(self._app_dir)

        fileName = ""
        fileName += str(self._app_code)
        fileName += "__"
        fileName += data_name
        fileName = fileName.upper()
        fileName += ".pkl"

        self._file = os.path.join(self._app_dir, fileName)

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
        with open(self._file, 'rb') as f:
            self.data = pickle.load(f)

    def save(self):
        """
        saves the data
        :return:
        """
        with open(self._file, 'wb') as f:
            pickle.dump(self.data, f)

    def update(self):
        self.load()

    def close(self):
        """
        saves and deletes self
        :return:
        """
        self.save()
        del self


if __name__ == "__main__":
    app = "new"
    name = "1"
    DI = data_interface(app_code=app)
