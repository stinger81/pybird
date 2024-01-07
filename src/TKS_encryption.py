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

# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
import os
import secrets

from Crypto import Random
from Crypto.Cipher import AES as _aes

import TCS_utils
import TCS_variables

class _AES:
    def __init__(self, key: str) -> None:
        self.version = TCS_utils.version()

        self._key = key

        self.aes = _aes


    def encrypt(self, raw:str):
        private_key = self._key.encode(TCS_variables.AES.ENCODING)
        raw = self.pad(raw)
        iv = Random.new().read(_aes.block_size)
        cipher = self.aes.new(private_key, _aes.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode(TCS_variables.AES.ENCODING)))


    def decrypt(self, enc:str):
        private_key = self._key.encode(TCS_variables.AES.ENCODING)
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = _aes.new(private_key, _aes.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))


    def pad(self, s):
        return s + (TCS_variables.AES.BLOCK_SIZE - len(s) % TCS_variables.AES.BLOCK_SIZE) * chr(
            TCS_variables.AES.BLOCK_SIZE - len(s) % TCS_variables.AES.BLOCK_SIZE)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

# class AES:
#     def __init__(self) -> None:
#         self.version = TCS_utils.version()
#
#         self.aes = _aes
#         self._aes_keychain = _AES_keychain()
#
#     def encrypt(self, raw):
#         private_key = self._aes_keychain._read_key().encode(TCS_variables.AES_ENCODING)
#         # print(private_key.decode())
#         raw = self.pad(raw)
#         iv = Random.new().read(_aes.block_size)
#         cipher = self.aes.new(private_key, _aes.MODE_CBC, iv)
#         return base64.b64encode(iv + cipher.encrypt(raw.encode(TCS_variables.AES_ENCODING)))
#
#     def decrypt(self, enc):
#         private_key = self._aes_keychain._read_key().encode(TCS_variables.AES_ENCODING)
#         enc = base64.b64decode(enc)
#         iv = enc[:16]
#         cipher = _aes.new(private_key, _aes.MODE_CBC, iv)
#         return self.unpad(cipher.decrypt(enc[16:]))
#
#     def pad(self, s):
#         return s + (TCS_variables.AES_BLOCK_SIZE - len(s) % TCS_variables.AES_BLOCK_SIZE) * chr(
#             TCS_variables.AES_BLOCK_SIZE - len(s) % TCS_variables.AES_BLOCK_SIZE)
#
#     def unpad(self, s):
#         return s[:-ord(s[len(s) - 1:])]

class AES_ENC(_AES):
    def __init__(self):
        self._aes_keychain = _AES_keychain()
        self._key = self._aes_keychain._read_key()
        super().__init__(self._key)

class AES_savekey(_AES):
    def __init__(self, app_name:str, save_key:str) -> None:
        encoded_key = str(app_name+save_key).encode(TCS_variables.AES.ENCODING)
        self._key = hashlib.sha256(encoded_key).hexdigest()[0:32]
        super().__init__(self._key)

class AES_savekey_ENC(_AES):
    def __init__(self, app_name:str, save_key:str) -> None:
        key_aes = AES_ENC()
        my_key = app_name+save_key
        my_key_enc = key_aes.encrypt(my_key)
        self._key = hashlib.sha256(my_key_enc).hexdigest()[0:32]
        del key_aes
        super().__init__(self._key)




class _AES_keychain:
    def __init__(self) -> None:
        self.version = TCS_utils.version()

    def _ui(self):
        while True:
            print()
            print("WARNING: THIS KEY SHOULD NOT BE SHARED WITH ANYONE")
            print("WARNING: Keys are stored in a scrambled state and can be decoded by anyone with this source code")
            print("AES menu")
            print("1 - Enter 256-bit Key")
            print("2 - Generate 265-bit key")
            print("q - Quit/Exit")
            print()
            user_input = input("Menu Selection [q]: ")
            print()
            if user_input == "q" or user_input == "":
                break
            elif user_input == "1":
                print("IMPORTANT READ THE FOLLOWING BEFORE PROCEEDING")
                print("""
By running this program, the current AES key will be permanently deleted. The new key 
that is entered will replace it. This operation can NOT be reversed This will causes 
all existing Twitter keys to be unusable by this software. All keys must be re-enter 
using "PYBIRDMgrUI.py". 
                """)
                print()
                user_input = input("Type 'CONFIRM' to continue: ")
                if user_input == "CONFIRM":
                    self._add_AES.key()
                    break
            elif user_input == "2":
                print("256-bit Key:")
                print(self.generate_key())

    def pad(self, s):
        return s + (TCS_variables.AES.BLOCK_SIZE - len(s) % TCS_variables.AES.BLOCK_SIZE) * chr(
            TCS_variables.AES.BLOCK_SIZE - len(s) % TCS_variables.AES.BLOCK_SIZE)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def _add_aes_key(self):
        _test_key = ""

        invalid_key: bool = True
        while invalid_key:
            print()
            _test_key: str = input("Enter a 256-bit key: ")
            _test_key_bytes: bytes = _test_key.encode(TCS_variables.AES.ENCODING)
            if len(_test_key_bytes) * 8 == 256:
                print()
                print("New Key")
                print("String: " + str(_test_key))
                print("Bytes: " + str(_test_key_bytes.hex()))
                print("IMPORTANT: This operation can not be reversed")
                print("IMPORTANT: This operation will make all keys un-useable")

                user_input = input("Type 'CONFIRM' to continue: ")
                if user_input == "CONFIRM":
                    invalid_key = False
            else:
                print()
                print("Invalid Key Must Be 256-bit(32 bytes) not " + str(len(_test_key_bytes) * 8) + " bits")

        if os.path.exists(TCS_variables.AES_KEY_FILE):
            print()
            print("Deleting old AES credentials")
            TCS_utils.copy_file_to_old(TCS_variables.AES_KEY_FILE)
            TCS_utils.delete_file(TCS_variables.AES_KEY_FILE)

        _key_hash = hashlib.sha512(_test_key.encode(TCS_variables.AES.ENCODING)).hexdigest()

        _encoded_key = self._encode_key(_test_key)

        _encoded_key_hash = hashlib.sha512(_encoded_key.encode(TCS_variables.AES.ENCODING)).hexdigest()

        TCS_utils.append_text_file(TCS_variables.AES_KEY_FILE, _encoded_key)
        TCS_utils.append_text_file(TCS_variables.AES_KEY_FILE, _key_hash)
        TCS_utils.append_text_file(TCS_variables.AES_KEY_FILE, _encoded_key_hash)

        print("AES key added!")
        # _test = self._read_key()
        # print("String: "+str(_test))
        # print("Bytes: "+str(_test.encode().hex()))

    def _read_key(self) -> str:
        if os.path.exists(TCS_variables.AES_KEY_FILE):
            with open(TCS_variables.AES_KEY_FILE, "r") as f:
                _raw_file = f.readlines()
                _encoded_key_file = _raw_file[0].strip("\n")
                _key_hash_file = _raw_file[1].strip("\n")
                _encoded_key_hash_file = _raw_file[2].strip("\n")

                if hashlib.sha512(
                        _encoded_key_file.encode(TCS_variables.AES.ENCODING)).hexdigest() == _encoded_key_hash_file:
                    # pre-decoding checksum
                    pass
                else:
                    raise TCS_variables.PYBIRDAESkeyERROR("Invalid Pre-Decoding Checksum")

                _decoded_key = self._decode_key(_encoded_key_file)

                if hashlib.sha512(_decoded_key.encode(TCS_variables.AES.ENCODING)).hexdigest() == _key_hash_file:
                    # post-decoding checksum
                    pass
                else:
                    raise TCS_variables.PYBIRDAESkeyERROR("Invalid Post-Decoding Checksum")
                return _decoded_key

                # return self._decode_key(_raw_key)
        else:
            raise TCS_variables.PYBIRDAESkeyERROR("AES Key file not found")

    def _encode_key(self, key: str):
        _b64_bytes: bytes = b""

        _bytes = key.encode(TCS_variables.AES.ENCODING)
        for passes in range(TCS_variables.AES.KEY_SCRAMBLE_LENGTH):
            _b64_bytes = base64.b64encode(_bytes)
            _bytes = _b64_bytes
            msg = "ENCODING STATUS: " + str(passes + 1) + " / " + str(TCS_variables.AES.KEY_SCRAMBLE_LENGTH)
            print(msg, end="\r")
        _b64 = _b64_bytes.decode(TCS_variables.AES.ENCODING)
        return _b64

    def _decode_key(self, key: str):
        _bytes: bytes = b""

        _b64_bytes: bytes = key.encode(TCS_variables.AES.ENCODING)
        for passes in range(TCS_variables.AES.KEY_SCRAMBLE_LENGTH):
            _bytes: bytes = base64.b64decode(_b64_bytes)
            _b64_bytes = _bytes
            # msg = "DECODING STATUS: "+str(passes+1)+" / "+str(TCS_variables.AES.KEY_SCRAMBLE_LENGTH)
            # print(msg,end = "\r")
        str_key: str = _bytes.decode(TCS_variables.AES.ENCODING)
        return (str_key)

    ################################################################################################
    # region generate keys
    def generate_key(self):
        key = secrets.token_hex(16)
        return key
        # endregion
    ################################################################################################


if __name__ == "__main__":
    aes = _AES_keychain()
    print(aes._read_key())
