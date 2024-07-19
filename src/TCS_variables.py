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
"""
TCS Platform
Provides constants to be used
"""
import os
import sys
from pathlib import Path
from platform import uname

from TCS_variables_const import *
from TCS_variables_error import *


def _make_path(path):
    """
    Make a path
    :param path:
    :return:
    """
    path = os.path.normpath(path)
    # print(path)
    os.makedirs(path, exist_ok=True)


####################################################################################################
# region init
# home location
HOME = ""
for i in range(len(sys.argv)):
    if sys.argv[i] in SYS_ARG.HOME:
        _home = sys.argv[i + 1]
        HOME = os.path.normpath(_home)
if HOME == "":
    HOME = Path.home()
HOME_DIRECTORY = HOME

# config file name
for i in SYS_ARG.CONFIG:
    for j in sys.argv:
        if i == j:
            try:
                FILE_NAMES.SERVER_CONFIG = sys.argv[sys.argv.index(i) + 1]
            except:
                raise PYBIRDPlatformError("No config file specified")

NETWORK_NAME = ""  # network name should only be used on development systems to replicate a existing server

for i in SYS_ARG.DEVENV:
    for j in sys.argv:
        if i == j:
            try:
                NETWORK_NAME = sys.argv[sys.argv.index(i) + 1].upper()
            except:
                raise PYBIRDPlatformError("No network name specified")


# endregion
####################################################################################################
####################################################################################################
# region Pybird Directories

@dataclass(frozen=True)
class PYBIRD_DIRECTORIES:
    try:
        PYBIRD_DIRECTORY = os.path.normpath(os.environ[PYBIRD_ENV.TAG])
    except KeyError:
        PYBIRD_DIRECTORY: str = os.path.abspath('.')
        if PYBIRD_DIRECTORY.endswith(DIRECTORY_NAME.SRC):
            PYBIRD_DIRECTORY = os.path.abspath('..')
    try:
        PYBIRD_REMOTE_APP_DIRECTORY = os.path.normpath(os.environ[PYBIRD_ENV.REMOTE_DIR_TAG])
    except KeyError:
        PYBIRD_REMOTE_APP_DIRECTORY: str = str(Path.home())

    SRC: str = os.path.join(PYBIRD_DIRECTORY, DIRECTORY_NAME.SRC)  # DO NOT MAKE DIR
    CONFIG: str = os.path.join(PYBIRD_DIRECTORY, DIRECTORY_NAME.CONFIG)  # DO NOT MAKE DIR
    ADD_CRED: str = os.path.join(PYBIRD_DIRECTORY, DIRECTORY_NAME.ADD_CRED)  # DO NOT MAKE DIR

    LOG: str = os.path.join(PYBIRD_DIRECTORY, DIRECTORY_NAME.LOG)
    _make_path(LOG)

    APP_LOCAL: str = os.path.join(PYBIRD_DIRECTORY, DIRECTORY_NAME.APP_LOCAL)
    _make_path(APP_LOCAL)

    ####################################################################################################
    # region DATA Directories

    DATA: str = os.path.join(PYBIRD_DIRECTORY, DIRECTORY_NAME.DATA)
    _make_path(DATA)

    DATA_LOG: str = os.path.join(DATA, DIRECTORY_NAME.LOG)
    _make_path(DATA_LOG)

    DATA_SESSION: str = os.path.join(DATA, DIRECTORY_NAME.SESSION)
    _make_path(DATA_SESSION)

    DATA_APPDATA: str = os.path.join(DATA, DIRECTORY_NAME.APPDATA, NETWORK_NAME)
    _make_path(DATA_APPDATA)

    # endregion
    ####################################################################################################
    # region HOME Directories .pybird

    PYBIRD_HOME: str = os.path.join(HOME_DIRECTORY, DIRECTORY_NAME.HOME_DATA)
    _make_path(PYBIRD_HOME)

    PYBIRD_HOME_NET: str = os.path.join(PYBIRD_HOME, NETWORK_NAME)

    PYBIRD_HOME_APP: str = os.path.join(PYBIRD_HOME_NET, DIRECTORY_NAME.HOME_DATA_APP)
    _make_path(PYBIRD_HOME_APP)

    PYBIRD_HOME_AES: str = os.path.join(PYBIRD_HOME_NET, DIRECTORY_NAME.HOME_DATA_AES)
    _make_path(PYBIRD_HOME_AES)

    @staticmethod
    def PYBIRD_APP_HOME_DIR(app_name: str) -> str:
        path = os.path.join(PYBIRD_DIRECTORIES.PYBIRD_HOME_APP, app_name.upper())
        _make_path(path)
        return path

    @staticmethod
    def PYBIRD_APP_ATLAS_DIR(app_name: str) -> str:
        path = os.path.join(PYBIRD_DIRECTORIES.PYBIRD_APP_HOME_DIR(app_name), DIRECTORY_NAME.HOME_DATA_ATLAS)
        _make_path(path)
        return path

    @staticmethod
    def PYBIRD_APP_X_DIR(app_name: str) -> str:
        path = os.path.join(PYBIRD_DIRECTORIES.PYBIRD_APP_HOME_DIR(app_name), DIRECTORY_NAME.HOME_DATA_X)
        _make_path(path)
        return path

    @staticmethod
    def PYBIRD_APP_GENERAL_DIR(app_name: str) -> str:
        path = os.path.join(PYBIRD_DIRECTORIES.PYBIRD_APP_HOME_DIR(app_name), DIRECTORY_NAME.HOME_DATA_GENERAL)
        _make_path(path)
        return path

    @staticmethod
    def PYBIRD_APP_ATLAS_KEY(app_name: str, key_name: str) -> str:
        return os.path.join(PYBIRD_DIRECTORIES.PYBIRD_APP_ATLAS_DIR(app_name),
                            key_name.upper() + FILE_EXTENSIONS.KEY_ATLAS)

    @staticmethod
    def PYBIRD_APP_X_KEY(app_name: str) -> str:
        return os.path.join(PYBIRD_DIRECTORIES.PYBIRD_APP_X_DIR(app_name), app_name.upper() + FILE_EXTENSIONS.KEY_X)

    @staticmethod
    def PYBIRD_APP_GENERAL_KEY(app_name: str, key_name: str) -> str:
        return os.path.join(PYBIRD_DIRECTORIES.PYBIRD_APP_GENERAL_DIR(app_name),
                            key_name.upper() + FILE_EXTENSIONS.KEY_GENERAL)

    @staticmethod
    def PYBIRD_APP_DATA_DIR(app_name: str) -> str:
        path = os.path.join(PYBIRD_DIRECTORIES.DATA_APPDATA, app_name.upper())
        _make_path(path)
        return path


# endregion
####################################################################################################

####################################################################################################
# region Predefined file names

# Linux
SYS_LINUX_UPTIME: str = "/proc/uptime"

# endregion
####################################################################################################

####################################################################################################
# region Platform configuration - set based on type of platform

PYBIRD_PLATFORM: str = PLATFORM.LINUX
try:
    TEMP_PLATFORM = os.environ[PYBIRD_ENV.PLATFORM_TAG]
    if TEMP_PLATFORM in [PLATFORM.WINDOWS,
                         PLATFORM.LINUX,
                         PLATFORM.MACOS,
                         PLATFORM.AWS_EC2_AMZ,
                         PLATFORM.AWS_EC2_UBUNTU,
                         PLATFORM.WSL,
                         PLATFORM.PI32,
                         PLATFORM.PI64]:
        PYBIRD_PLATFORM = TEMP_PLATFORM

    else:
        raise PYBIRDPlatformError("PYBIRD_PLATFORM is not supported")
except:
    if sys.platform.startswith(PLATFORM_CHECK.WINDOWS):
        PYBIRD_PLATFORM = PLATFORM.WINDOWS
    elif sys.platform.startswith(PLATFORM_CHECK.MACOS):
        PYBIRD_PLATFORM = PLATFORM.MACOS
    elif sys.platform.startswith(PLATFORM_CHECK.LINUX):
        if PLATFORM_CHECK.WSL in uname().release:
            PYBIRD_PLATFORM = PLATFORM.WSL
        else:
            PYBIRD_PLATFORM = PLATFORM.LINUX
    else:
        PYBIRD_PLATFORM = PLATFORM.UNKNOWN

try:
    PYTHON_COMMAND_LINE_STRING: str = os.environ[PYBIRD_ENV.PYTHON_TAG]
except:
    PYTHON_COMMAND_LINE_STRING: str = DEFAULT.COMMAND_LINE_KEY

# endregion
####################################################################################################

####################################################################################################
# region Keychain Data

AES_KEY_FILE = os.path.join(PYBIRD_DIRECTORIES.PYBIRD_HOME_AES, AES.KEY_FILE_NAME)

# endregion
####################################################################################################


####################################################################################################
# region OS Specific Settings
if PYBIRD_PLATFORM == PLATFORM.WINDOWS:  # Windows 10/11
    PLATFORM_UNIX_BASED = False
    PLATFORM_REMOTE_SERVER = False

elif PYBIRD_PLATFORM == PLATFORM.LINUX:  # General Linux
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = False

elif PYBIRD_PLATFORM == PLATFORM.MACOS:  # MacOS
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = False

elif PYBIRD_PLATFORM == PLATFORM.WSL:  # Windows Subsystem for Linux
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = False

elif PYBIRD_PLATFORM == PLATFORM.AWS_EC2_AMZ:  # AWS EC2 (Amazon Linux 2) Server
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = True

elif PYBIRD_PLATFORM == PLATFORM.AWS_EC2_UBUNTU:  # AWS EC2 (Amazon Linux 2023) Server
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = True

elif PYBIRD_PLATFORM == PLATFORM.PI32:  # Raspberry Pi OS 32 Bit
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = False

elif PYBIRD_PLATFORM == PLATFORM.PI64:  # Raspberry Pi OS 64 Bit
    PLATFORM_UNIX_BASED = True
    PLATFORM_REMOTE_SERVER = False
else:
    PLATFORM_UNIX_BASED = False
    PLATFORM_REMOTE_SERVER = False

# endregion
####################################################################################################
