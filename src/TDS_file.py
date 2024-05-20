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
from contextlib import contextmanager

import TCS_variables
import TKS_encryption
import TCS_utils


class TDS_file:
    def __init__(self, appName, save_key=""):
        self.appName = appName
        self.saveKey = save_key
        self._app_dir = TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_APP_DATA_DIR(self.appName)
        if save_key == "":
            self.encryption = False
        else:
            self.encryption = True
            self._my_aes = TKS_encryption.AES_savekey(app_name=self.appName, save_key=self.saveKey)

    def open(self, file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):

        my_file = os.path.join(self._app_dir, file)
        if self.encryption:
            return openFileEnc(file=my_file,
                               aes=self._my_aes,
                               mode=mode,
                               buffering=buffering,
                               encoding=encoding,
                               errors=errors,
                               newline=newline,
                               closefd=closefd,
                               opener=opener)
        else:
            return openFile(file=my_file,
                            mode=mode,
                            buffering=buffering,
                            encoding=encoding,
                            errors=errors,
                            newline=newline,
                            closefd=closefd,
                            opener=opener)

    def exists(self, filename):
        my_file = os.path.join(self._app_dir, filename)
        if self.encryption:
            my_file = my_file + ".enc"
        return os.path.exists(my_file)


@contextmanager
def openFile(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    f = open(file=file,
             mode=mode,
             buffering=buffering,
             encoding=encoding,
             errors=errors,
             newline=newline,
             closefd=closefd,
             opener=opener)
    try:
        yield f
    finally:
        f.close()


@contextmanager
def openFileEnc(file, aes, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    if "b" in mode:
        write = "wb"
        read = "rb"
    else:
        write = "w"
        read = "r"

    filename_enc = file + ".enc"
    filename_temp = file + ".__temp__"

    if os.path.isfile(filename_enc):
        with open(filename_enc, "rb") as f1:
            data_enc = f1.read()
            data = aes.decrypt(data_enc, _type=bytes)
            with open(filename_temp, write) as f2:
                if 'b' not in mode:
                    data = data.decode(TCS_variables.AES.ENCODING)
                f2.write(data)

    f = open(file=filename_temp,
             mode=mode,
             buffering=buffering,
             encoding=encoding,
             errors=errors,
             newline=newline,
             closefd=closefd,
             opener=opener)
    try:
        yield f
    finally:
        f.close()

    if os.path.isfile(filename_enc):
        TCS_utils.copy_file_to_old(filename_enc)
    with open(filename_temp, read) as f1:
        new_data = f1.read()
        data = aes.encrypt(new_data)
        with open(filename_enc, "wb+") as f2:
            f2.write(data)
    os.remove(filename_temp)


if __name__ == "__main__":
    file = TDS_file("MYTEST", "")
    with file.open("test.txt", "wb") as f:
        f.write(b"Hello World")
    with file.open("test.txt", "rb") as f:
        print(f.read())
    file = TDS_file("MYTEST", "1234567890")
    with file.open("test.txt", "wb") as f:
        f.write(b"Hello World")
    with file.open("test.txt", "rb") as f:
        print(f.read())
