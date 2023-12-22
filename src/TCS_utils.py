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

import shutil
import os
import time

import TCS_variables

LICENSE = """
    PYBIRD a app based framework for social media management.
    Copyright (C) 2022-2023  Michael Dompke (https://github.com/stinger81)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class _version:
    def __init__(self):
        self.major: int = 0
        self.minor: int = 0
        self.patch: int = 0
        self.build: int = 0

        self.release_candidate: bool = False
        self.beta: bool = False
        self.alpha: bool = False
        self.dev: bool = False
        self.pre: bool = False

        self.name: str = str(None)
        self.description: str = str(None)
        self.author: str = str(None)
        self.email: str = str(None)
        self.url: str = str(None)
        self.license: str = str(None)

    def __str__(self):
        version_string = f"{self.major}.{self.minor}"
        if self.patch > 0 or self.build != 0:
            version_string += f".{self.patch}"
        if self.build > 0:
            version_string += f".{self.build}"

        if self.pre:
            version_string += "-pre"

        if self.release_candidate:
            version_string += "-rc"
        elif self.beta:
            version_string += "-beta"
        elif self.alpha:
            version_string += "-alpha"
        elif self.dev:
            version_string += "-dev"

        return version_string

    def short_str(self):
        version_string = f"{self.major}.{self.minor}"
        if self.patch > 0 or self.build != 0:
            version_string += f".{self.patch}"
        if self.build > 0:
            version_string += f".{self.build}"

        if self.dev:
            version_string += "-DEV"
        elif self.pre and self.alpha:
            version_string += "-PA"
        elif self.alpha:
            version_string += "-A"
        elif self.beta:
            version_string += "-B"
        elif self.release_candidate:
            version_string += "-RC"

        return version_string

    def full_str(self):
        version_string = f"{self.major}.{self.minor}.{self.patch}.{self.build}"

        if self.pre:
            version_string += "-pre"

        if self.release_candidate:
            version_string += "-rc"
        elif self.beta:
            version_string += "-beta"
        elif self.alpha:
            version_string += "-alpha"
        elif self.dev:
            version_string += "-dev"

        return version_string


class version(_version):
    def __init__(self):
        super().__init__()
        self.major = TCS_variables.PYBIRD_VER_MAJOR
        self.minor = TCS_variables.PYBIRD_VER_MINOR
        self.patch = TCS_variables.PYBIRD_VER_PATCH
        self.build = TCS_variables.PYBIRD_VER_BUILD
        self.pre = TCS_variables.PYBIRD_VER_PRE
        self.release_candidate = TCS_variables.PYBIRD_VER_RC
        self.beta = TCS_variables.PYBIRD_VER_BETA
        self.alpha = TCS_variables.PYBIRD_VER_ALPHA
        self.dev = TCS_variables.PYBIRD_VER_DEV


class app_version(_version):
    def __init__(self):
        super().__init__()


####################################################################################################
# region file management
def rename_file(in_filename: str = '', in_new_filename: str = ''):
    """
    Rename a file
    :param in_filename:  str - Original target_filename
    :param in_new_filename: str - New target_filename
    :return: bool - True if file exists and was renamed
    """
    if len(in_filename) > 0 and len(in_new_filename) > 0:
        try:
            os.rename(in_filename, in_new_filename)
            return True
        except (IOError, OSError):
            return False
    return False


def copy_file(in_filename: str = '', in_new_filename: str = ''):
    """
    Copy a file
    :param in_filename:  str - Original target_filename
    :param in_new_filename: str - New target_filename
    :return: bool - True if file exists and was copied
    """
    if len(in_filename) > 0 and len(in_new_filename) > 0:
        try:
            shutil.copyfile(in_filename, in_new_filename)
            return True
        except (IOError, OSError):
            return False
    return False


def move_file(in_filename: str = '', in_new_filename: str = ''):
    """
    Move a file
    :param in_filename:  str - Original target_filename
    :param in_new_filename: str - New target_filename
    :return: bool - True if file exists and was moved
    """
    if len(in_filename) > 0 and len(in_new_filename) > 0:
        try:
            shutil.move(in_filename, in_new_filename)
            return True
        except (IOError, OSError):
            return False
    return False


def rename_file_from_old(in_filename: str = ''):
    """
    Rename a from target_filename.old to target_filename
    :param in_filename:  str - Original target_filename
    :return: bool - True if file exists and was renamed
    """
    if len(in_filename) > 0 and os.path.exists(in_filename + '.old'):
        try:
            os.remove(in_filename)
        except (IOError, OSError):
            pass
        try:
            os.rename(in_filename + '.old', in_filename)
            return True
        except (IOError, OSError):
            return False
    return False


def rename_file_to_old(in_filename: str = ''):
    """
    Rename a file to target_filename.old
    :param in_filename:  str - Original target_filename
    :return: bool - True if file exists and was renamed
    """
    if len(in_filename) > 0:
        try:
            os.remove(in_filename + '.old')
        except (IOError, OSError):
            pass
        try:
            os.rename(in_filename, in_filename + '.old')
            return True
        except (IOError, OSError):
            return False
    return False


def copy_file_to_old(in_filename: str = '') -> str:
    """
    Copy a file to target_filename.old
    :param in_filename:  str - Original target_filename
    :return: Renamed filename (''None'' if fails)
    """
    my_new_name = ''
    if len(in_filename) > 0:
        my_new_name = in_filename + '.old'
        try:
            os.remove(my_new_name)
        except (IOError, OSError):
            pass
        try:
            shutil.copyfile(in_filename, my_new_name)
            return my_new_name
        except (IOError, OSError):
            return ''
    return my_new_name


def delete_file(in_filename: str = '') -> bool:
    """
    Delete a file (and any target_filename.old found)
    :param in_filename:  str - Original target_filename
    :return: bool -True if file exists and was deleted
    """
    if len(in_filename) > 0:
        try:
            os.remove(in_filename + '.old')
        except (IOError, OSError):
            pass
        try:
            os.remove(in_filename)
            return True
        except (IOError, OSError):
            return False
    return False


def delete_file_w_exc(in_filename: str = '') -> str:
    """
    Delete a file (and any target_filename.old found)
    :param in_filename:  str - Original target_filename
    :return: bool -True if file exists and was deleted
    """
    if len(in_filename) > 0:
        try:
            os.remove(in_filename + '.old')
        except (IOError, OSError):
            pass
        try:
            os.remove(in_filename)
            return ''
        except (IOError, OSError) as exc:
            return str(exc)
    return ''


def append_text_file(in_filename: str, in_string: str):
    """
    Append a string to a text file (create the file if it does not exist)
    :param in_filename: str - Filename
    :param in_string: str - String to append
    :return: None
    """
    try:
        with open(in_filename, "a") as my_file:
            my_file.write(in_string + '\n')
    except (IOError, OSError):
        pass


def append_text_file_restricted_file_length(in_filename: str, in_string: str, max_length: int = -1):
    """
    Append a string to a text file (create the file if it does not exist)
    :param in_filename: str - Filename
    :param in_string: str - String to append
    :param max_length: int - max number of lines in the file not including the header (-1 == no restrictions)
    :return: None
    """
    try:
        with open(in_filename, "r") as my_file:
            lines = my_file.readlines()
            file_length = len(lines) - 1
    except (IOError, OSError):
        lines = []
        file_length = 0

    if max_length == -1:  # no restrictions
        # print("no restrictions")
        append_text_file(in_filename, in_string)

    elif file_length < max_length:  # append to file
        # print("not exceded")
        append_text_file(in_filename, in_string)

    else:  # remove the number of lines that exceed the limit
        print("removing")
        delta = file_length - max_length + 2
        print(delta)
        my_lines = [lines[0]]
        my_lines.extend(lines[delta:])
        with open(in_filename, "w") as my_file:
            my_file.writelines(my_lines)
        append_text_file(in_filename, in_string)


# endregion

####################################################################################################

####################################################################################################
# region data types conversions

# str to bool conversion
def str_to_bool(in_str: str) -> bool:
    if in_str.lower().strip() == 'true':
        return True
    else:
        return False


# bool to str conversion
def bool_to_str(in_bool: bool) -> str:
    if in_bool:
        return "True"
    else:
        return "False"


# str to int conversion
def str_to_int(in_str: str) -> int:
    return int(in_str)


# int to string conversion
def int_to_str(in_int: int) -> str:
    return str(in_int)


# delimitated list to python list str
def delimitated_to_list_str(in_list: str, in_delimiter: str = ','):
    return in_list.split(in_delimiter)


# delimited list to python list int
def delimitated_to_list_int(in_list: str, in_delimiter: str = ','):
    return [int(x) for x in in_list.split(in_delimiter)]


# endregion
####################################################################################################
####################################################################################################
# region user input utilities

def getUserInput(in_prompt: str = '', in_default: str = '') -> str:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_default: str - Default value
    :return: str - User input
    """
    my_question = in_prompt + ' [' + in_default + ']: '
    my_input = input(my_question)
    if my_input == '':
        my_input = in_default
    return my_input


def getUserInput_yn(in_prompt: str = '', in_default: str = 'n') -> bool:
    """
    Get a yes or no from the user
    :param in_prompt: str - Prompt to display
    :param in_default: bool - Default value
    :return: bool - True if yes
    """
    my_question = in_prompt + '(y/n)'
    while True:
        my_input = getUserInput(my_question, in_default)
        if my_input.lower() == 'y' or my_input.lower() == 'n':
            break
        else:
            print("Invalid input must be 'y' or 'n'")

    if my_input.lower() == 'y':
        return True
    else:
        return False


def getUserInput_int(in_prompt: str = '', in_default: int = 0) -> int:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_default: int - Default value
    :return: int - User input
    """
    while True:
        my_input = getUserInput(in_prompt, str(in_default))
        try:
            my_input = int(my_input)
            break
        except ValueError:
            print("Invalid input must be an integer")
    return my_input


def getUserInput_float(in_prompt: str = '', in_default: float = 0.0) -> float:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_default: float - Default value
    :return: float - User input
    """
    while True:
        my_input = getUserInput(in_prompt, str(in_default))
        try:
            my_input = float(my_input)
            break
        except ValueError:
            print("Invalid input must be a float")
    return my_input


def getUserInput_listChoice(in_prompt: str = '', in_options: list = [], in_default: int = 0):
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_options: list - list of options
    :param in_default: int - Default value
    :return: int - User input
    """
    if len(in_options) == 0:
        return None
    while True:
        for i in range(len(in_options)):
            print(str(i) + " - " + in_options[i])
        my_input = getUserInput(in_prompt, str(in_default))
        try:
            my_input = int(my_input)
            if my_input < len(in_options):
                break
            else:
                print("Value out of range")
        except ValueError:
            print("Invalid input must be an integer")
    return in_options[my_input]


def getUserInput_Confirm(in_prompt: str = '', in_confirmation_code: str = 'y', case_sensitive: bool = False) -> bool:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_confirmation_code: str - Confirmation code
    :param case_sensitive: bool - True if case sensitive
    :return: bool - User input
    """
    my_prompt = in_prompt + ' (' + in_confirmation_code + ')'
    if case_sensitive:
        my_prompt += ' CASE-SENSITIVE'
    my_input = getUserInput(my_prompt, '')
    if case_sensitive:
        if my_input == in_confirmation_code:
            return True
        else:
            return False
    else:
        if my_input.lower() == in_confirmation_code.lower():
            return True
        else:
            return False


# endregion
####################################################################################################
if __name__ == '__main__':
    # v = version()
    # v.major = 1
    # v.minor = 2
    # v.patch = 3
    # v.build = 4
    # print(v)

    import os

    test_file = 'test.txt'
    test_file = os.path.join(os.getcwd(), test_file)
    for i in range(10):
        #     append_text_file(test_file, str('test'+str(i)))
        append_text_file_restricted_file_length(test_file, str('test' + str(i)), 5)
        time.sleep(5)
