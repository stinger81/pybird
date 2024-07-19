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
import shutil
import sys
from typing import Union, List

import TCS_variables

LICENSE = """
    PYBIRD a app based framework for social media management.
    Copyright (C) 2022-2024  Michael Dompke (https://github.com/stinger81)

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
        """
        Short version string
        :return:
        """
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
        """
        Full version string
        :return:
        """
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
        self.major = TCS_variables.PYBIRD_VER.MAJOR
        self.minor = TCS_variables.PYBIRD_VER.MINOR
        self.patch = TCS_variables.PYBIRD_VER.PATCH
        self.build = TCS_variables.PYBIRD_VER.BUILD
        self.pre = TCS_variables.PYBIRD_VER.PRE
        self.release_candidate = TCS_variables.PYBIRD_VER.RC
        self.beta = TCS_variables.PYBIRD_VER.BETA
        self.alpha = TCS_variables.PYBIRD_VER.ALPHA
        self.dev = TCS_variables.PYBIRD_VER.DEV


class app_version(_version):
    def __init__(self):
        super().__init__()


####################################################################################################
# region file management


def tree(path: str = '.', level: int = 0, max_level: int = -1):
    """
    Display a tree of the files and folders in a path
    :param path: str - Path to display
    :param level: int - Level of the tree
    :param max_level: int - Max level of the tree (-1 == no limit)
    :return: None
    """
    if max_level == -1 or level <= max_level:
        for f in os.listdir(path):
            print('|   ' * level + '|-> ' + f)
            if os.path.isdir(os.path.join(path, f)):
                tree(os.path.join(path, f), level + 1, max_level)


def pybird_keychain_tree():
    """
    Display a tree of the files and folders in the keychain
    :return:
    """
    my_path = TCS_variables.PYBIRD_DIRECTORIES.PYBIRD_HOME
    tree(my_path, 0, -1)


def pybird_data_tree():
    """
    Display a tree of the files and folders in the data directory
    :return:
    """
    my_path = TCS_variables.PYBIRD_DIRECTORIES.DATA
    tree(my_path, 0, -1)


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
        with open(in_filename, "a", encoding="utf-8") as my_file:
            my_file.write(in_string + '\n')
    except (IOError, OSError) as e:
        if TCS_variables.SYS_ARG.RAISE[0] in sys.argv:
            raise e


def append_text_file_restricted_file_length(in_filename: str, in_string: str, max_length: int = -1):
    """
    Append a string to a text file (create the file if it does not exist)
    :param in_filename: str - Filename
    :param in_string: str - String to append
    :param max_length: int - max number of lines in the file not including the header (-1 == no restrictions)
    :return: None
    """
    try:
        with open(in_filename, "r", encoding="utf-8") as my_file:
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
        with open(in_filename, "w", encoding="utf-8") as my_file:
            my_file.writelines(my_lines)
        append_text_file(in_filename, in_string)


# endregion

####################################################################################################

####################################################################################################
# region data types conversions

# str to bool conversion
def str_to_bool(in_str: str) -> bool:
    """
    Convert a string to a bool
    :param in_str:
    :return:
    """
    if in_str.lower().strip() == 'true':
        return True
    else:
        return False


# bool to str conversion
def bool_to_str(in_bool: bool) -> str:
    """
    Convert a bool to a string
    :param in_bool:
    :return:
    """
    if in_bool:
        return "True"
    else:
        return "False"


# str to int conversion
def str_to_int(in_str: str) -> int:
    """
    Convert a string to an int
    :param in_str:
    :return:
    """
    return int(in_str)


# int to string conversion
def int_to_str(in_int: int) -> str:
    """
    Convert an int to a string
    :param in_int:
    :return:
    """
    return str(in_int)


# delimitated list to python list str
def delimitated_to_list_str(in_list: str, in_delimiter: str = ','):
    """
    Convert a delimited list to a python list
    :param in_list:
    :param in_delimiter:
    :return:
    """
    return in_list.split(in_delimiter)


# delimited list to python list int
def delimitated_to_list_int(in_list: str, in_delimiter: str = ','):
    """
    Convert a delimited list to a python list
    :param in_list:
    :param in_delimiter:
    :return:
    """
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


def getUserInput_listChoiceMulti(in_prompt: str = '', in_options: list = [], in_default: int = 0):
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_options: list - list of options
    :param in_default: int - Default value
    :return: int - User input
    """
    in_prompt += " (comma separated list)"
    if len(in_options) == 0:
        return None
    while True:
        for i in range(len(in_options)):
            print(str(i) + " - " + in_options[i])
        my_input: str = getUserInput(in_prompt, str(in_default))
        # print(my_input)
        my_input_list = my_input.split(',')
        my_output_list = []
        # print(my_input_list)
        all_pass = True
        try:
            for i in my_input_list:
                if int(i) >= len(in_options):
                    print("Value out of range: " + str(i))
                    raise ValueError
                else:
                    my_output_list.append(in_options[int(i)])
        except ValueError:
            all_pass = False
            print("Invalid input must be an integer")
        if all_pass:
            break
    return my_output_list


def getUserInput_Confirm(in_prompt: str = '', in_confirmation_code: str = 'y', in_case_sensitive: bool = False) -> bool:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_confirmation_code: str - Confirmation code
    :param case_sensitive: bool - True if case sensitive
    :return: bool - User input
    """
    my_prompt = in_prompt + ' (' + in_confirmation_code + ')'
    if in_case_sensitive:
        my_prompt += ' CASE-SENSITIVE'
    my_input = getUserInput(my_prompt, '')
    if in_case_sensitive:
        if my_input == in_confirmation_code:
            return True
        else:
            return False
    else:
        if my_input.lower() == in_confirmation_code.lower():
            return True
        else:
            return False


def getUserInput_required_length(in_prompt: str = '', in_length: int = 0) -> str:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_length: int - Required length
    :return: str - User input
    """
    while True:
        my_input = getUserInput(in_prompt, '')
        if len(my_input) == in_length:
            break
        else:
            print("Invalid input must be " + str(in_length) + " characters")
    return my_input


def getUserInput_required_minimum_length(in_prompt: str = '', in_length: int = 0) -> str:
    """
    Get user input
    :param in_prompt: str - Prompt to display
    :param in_length: int - Required length
    :return: str - User input
    """
    while True:
        my_input = getUserInput(in_prompt, '')
        if len(my_input) >= in_length:
            break
        else:
            print("Invalid input must be at least " + str(in_length) + " characters")
    return my_input


# endregion
####################################################################################################

####################################################################################################
# region sys args reader

def arg_in_sys_args(in_arg: List) -> bool:
    """
    Check if an argument is in sys.args
    :param in_arg: str - Argument to check
    :return: bool - True if argument is in sys.args
    """
    for arg in in_arg:
        if arg in sys.argv:
            return True
    return False


def get_arg_value(in_arg: List, in_default: str = None) -> Union[None, str]:
    """
    Get the value of an argument
    :param in_arg: str - Argument to check
    :return: str - Value of the argument
    """
    for arg in in_arg:
        if arg in sys.argv:
            try:
                return sys.argv[sys.argv.index(arg) + 1]
            except IndexError:
                return in_default
    return in_default


def get_arg_value_int(in_arg: List, in_default: int = None) -> Union[None, int]:
    """
    Get the value of an argument
    :param in_arg: str - Argument to check
    :return: int - Value of the argument
    """
    my_val = get_arg_value(in_arg)
    try:
        return int(my_val)
    except ValueError:
        return in_default


def get_arg_value_float(in_arg: List, in_default: float = None) -> Union[None, float]:
    """
    Get the value of an argument
    :param in_arg: str - Argument to check
    :return: float - Value of the argument
    """
    my_val = get_arg_value(in_arg)
    try:
        return float(my_val)
    except ValueError:
        return in_default


def get_arg_value_bool(in_arg: List,
                       in_if_exist_default: bool = True,
                       in_default: Union[bool, None] = None) -> Union[None, bool]:
    """
    Get the value of an argument
    :param in_arg: str - Argument to check
    :return: bool - Value of the argument
    """
    exist = arg_in_sys_args(in_arg)
    if exist:
        my_val = get_arg_value(in_arg)
        try:
            if my_val.lower() in ['true', 't', 'yes', 'y']:
                return True
            elif my_val.lower() in ['false', 'f', 'no', 'n']:
                return False
            else:
                return in_if_exist_default
        except ValueError:
            return in_if_exist_default
        except AttributeError:
            return in_if_exist_default
    else:
        return in_default


# endregion
###W###############################################################################################

####################################################################################################
# bytes size management
class ByteSize(int):
    _KB = 1024
    _suffixes = 'B', 'KB', 'MB', 'GB', 'PB'

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.bytes = self.B = int(self)
        self.kilobytes = self.KB = self / self._KB ** 1
        self.megabytes = self.MB = self / self._KB ** 2
        self.gigabytes = self.GB = self / self._KB ** 3
        self.petabytes = self.PB = self / self._KB ** 4
        *suffixes, last = self._suffixes
        suffix = next((
            suffix
            for suffix in suffixes
            if 1 < getattr(self, suffix) < self._KB
        ), last)
        self.readable = suffix, getattr(self, suffix)

        super().__init__()

    def __str__(self):
        return self.__format__('.2f')

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def __format__(self, format_spec):
        suffix, val = self.readable
        return '{val:{fmt}} {suf}'.format(val=val, fmt=format_spec, suf=suffix)

    def __sub__(self, other):
        return self.__class__(super().__sub__(other))

    def __add__(self, other):
        return self.__class__(super().__add__(other))

    def __mul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rsub__(self, other):
        return self.__class__(super().__sub__(other))

    def __radd__(self, other):
        return self.__class__(super().__add__(other))

    def __rmul__(self, other):
        return self.__class__(super().__rmul__(other))


# endregion
####################################################################################################
if __name__ == '__main__':
    # v = version()
    # v.major = 1
    # v.minor = 2
    # v.patch = 3
    # v.build = 4
    # print(v)

    tree()

    # import os
    #
    # test_file = 'test.txt'
    # test_file = os.path.join(os.getcwd(), test_file)
    # for i in range(10):
    #     #     append_text_file(test_file, str('test'+str(i)))
    #     append_text_file_restricted_file_length(test_file, str('test' + str(i)), 5)
    #     time.sleep(5)
