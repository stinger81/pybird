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
"""
TCS Platform
Provides constants to be used
"""
import os
import sys
from pathlib import Path
from platform import uname

from TCS_variables_error import *

#####################################################################################################
# region version

PYBIRD_VER_MAJOR = 0
PYBIRD_VER_MINOR = 8
PYBIRD_VER_PATCH = 6
PYBIRD_VER_BUILD = 0
PYBIRD_VER_PRE = True
PYBIRD_VER_RC = False
PYBIRD_VER_BETA = False
PYBIRD_VER_ALPHA = True
PYBIRD_VER_DEV = False

# endregion
####################################################################################################
####################################################################################################
# region Environment variables
# Must also be changed in TBS_bootloader_vars.py
PYBIRD_TAG = 'PYBIRD'
PYBIRD_REMOTE_DIR_TAG = 'PYBIRDRemoteDir'
PYBIRD_PLATFORM_TAG = 'PYBIRDPlatform'
PYBIRD_PYTHON_TAG = 'PYBIRDPython'

# endregion
####################################################################################################
####################################################################################################
# region file names
PYBIRD_NODE_CONFIG_ENDING = '_NODE_CONFIG.csv'
# endregion 
####################################################################################################
####################################################################################################
# region init home
HOME = ""
for i in range(len(sys.argv)):
    if sys.argv[i] == "-boot":
        _home_list = sys.argv[i + 1].split("/")
        HOME = os.path.join("/", *_home_list)
        print("WARNING: -boot is only supported on Linux")
if HOME == "":
    HOME = Path.home()
HOME_DIRECTORY = HOME
# endregion
####################################################################################################
####################################################################################################
# region session info
SESSION_DATETIME_FORMAT = "%Y%m%d%H%M%S%f%z"
SESSION_FILE_EXTENSION = ".sessionID"
SESSION_UNIQUE_ID_LENGTH = 8  # MD5 hash, max length of 32

# endregion
####################################################################################################
####################################################################################################
# region Base Directories
PYBIRD_HOME_DIRNAME = '.pybird'
PYBIRD_SRC_DIRNAME = 'src'
PYBIRD_LOG_DIRNAME = 'log'
PYBIRD_CONFIG_DIRNAME = 'config'
PYBIRD_APP_LOCAL_DIRNAME = 'PYBIRD_APPS'
PYBIRD_DATA_DIRNAME = 'data'
PYBIRD_SESSION_DIRNAME = 'session'
PYBIRD_APPDATA_DIRNAME = 'appdata'
PYBIRD_ADD_CRED_DIRNAME = "add_cred"

PYBIRD_HOME_APP_DIR = '.app'
PYBIRD_HOME_AES_DIR = '.aes'
PYBIRD_HOME_ATLAS_DIR = '.atlas'
try:
    PYBIRD_DIRECTORY = os.environ[PYBIRD_TAG]
except KeyError:
    PYBIRD_DIRECTORY: str = os.path.abspath('.')
    if PYBIRD_DIRECTORY.endswith(PYBIRD_SRC_DIRNAME):
        PYBIRD_DIRECTORY = os.path.abspath('..')
try:
    PYBIRD_REMOTE_APP_DIRECTORY = os.environ[PYBIRD_REMOTE_DIR_TAG]
except KeyError:
    PYBIRD_REMOTE_APP_DIRECTORY: str = str(Path.home())

PYBIRD_SRC_DIRECTORY: str = os.path.join(PYBIRD_DIRECTORY, PYBIRD_SRC_DIRNAME)
PYBIRD_CONFIG_DIRECTORY: str = os.path.join(PYBIRD_DIRECTORY, PYBIRD_CONFIG_DIRNAME)

PYBIRD_LOG_DIRECTORY: str = os.path.join(PYBIRD_DIRECTORY, PYBIRD_LOG_DIRNAME)
if not os.path.exists(PYBIRD_LOG_DIRECTORY):
    os.mkdir(PYBIRD_LOG_DIRECTORY)

PYBIRD_APP_LOCAL_DIRECTORY: str = os.path.join(PYBIRD_DIRECTORY, PYBIRD_APP_LOCAL_DIRNAME)
if not os.path.exists(PYBIRD_APP_LOCAL_DIRECTORY):
    os.mkdir(PYBIRD_APP_LOCAL_DIRECTORY)

PYBIRD_DATA_DIRECTORY: str = os.path.join(PYBIRD_DIRECTORY, PYBIRD_DATA_DIRNAME)
if not os.path.exists(PYBIRD_DATA_DIRECTORY):
    os.mkdir(PYBIRD_DATA_DIRECTORY)

PYBIRD_DATA_LOG_DIRECTORY: str = os.path.join(PYBIRD_DATA_DIRECTORY, PYBIRD_LOG_DIRNAME)
if not os.path.exists(PYBIRD_DATA_LOG_DIRECTORY):
    os.mkdir(PYBIRD_DATA_LOG_DIRECTORY)

PYBIRD_DATA_SESSION_DIRECTORY: str = os.path.join(PYBIRD_DATA_DIRECTORY, PYBIRD_SESSION_DIRNAME)
if not os.path.exists(PYBIRD_DATA_SESSION_DIRECTORY):
    os.mkdir(PYBIRD_DATA_SESSION_DIRECTORY)

PYBIRD_DATA_APPDATA_DIRECTORY: str = os.path.join(PYBIRD_DATA_DIRECTORY, PYBIRD_APPDATA_DIRNAME)
if not os.path.exists(PYBIRD_DATA_APPDATA_DIRECTORY):
    os.mkdir(PYBIRD_DATA_APPDATA_DIRECTORY)

PYBIRD_ADD_CRED_DIRECTORY: str = os.path.join(PYBIRD_DIRECTORY, PYBIRD_ADD_CRED_DIRNAME)  # DO NOT MAKE DIR

# .pybird
PYBIRD_HOME_DATA_DIRECTORY: str = os.path.join(HOME_DIRECTORY, PYBIRD_HOME_DIRNAME)

if not os.path.exists(PYBIRD_HOME_DATA_DIRECTORY):
    os.mkdir(PYBIRD_HOME_DATA_DIRECTORY)

PYBIRD_HOME_APP_DIRECTORY: str = os.path.join(PYBIRD_HOME_DATA_DIRECTORY, PYBIRD_HOME_APP_DIR)
if not os.path.exists(PYBIRD_HOME_APP_DIRECTORY):
    os.mkdir(PYBIRD_HOME_APP_DIRECTORY)

PYBIRD_HOME_AES_DIRECTORY: str = os.path.join(PYBIRD_HOME_DATA_DIRECTORY, PYBIRD_HOME_AES_DIR)
if not os.path.exists(PYBIRD_HOME_AES_DIRECTORY):
    os.mkdir(PYBIRD_HOME_AES_DIRECTORY)

PYBIRD_HOME_ATLAS_DIRECTORY: str = os.path.join(PYBIRD_HOME_DATA_DIRECTORY, PYBIRD_HOME_ATLAS_DIR)
if not os.path.exists(PYBIRD_HOME_ATLAS_DIRECTORY):
    os.mkdir(PYBIRD_HOME_ATLAS_DIRECTORY)

# endregion
####################################################################################################

####################################################################################################
# region Predefined file names

# Linux
SYS_LINUX_BOOT_LOG: str = os.path.join(HOME_DIRECTORY, "last_boot.txt")
SYS_LINUX_UPTIME: str = "/proc/uptime"

# endregion
####################################################################################################

####################################################################################################
# region Platform configuration - set based on type of platform
PLATFORM_CHECK_WINDOWS: str = "win"
PLATFORM_CHECK_LINUX: str = "linux"
PLATFORM_CHECK_MACOS: str = "darwin"
PLATFORM_CHECK_WSL: str = "microsoft-standard"

PYBIRD_PLATFORM_WINDOWS: str = 'windows'  # windows 10/11
PYBIRD_PLATFORM_LINUX: str = 'linux'  # general linux
PYBIRD_PLATFORM_MACOS: str = "macos"  # MacOS
PYBIRD_PLATFORM_AWS_EC2_LINUX2: str = "aws-ec2-linux2"  # AWS EC2 (Amazon Linux 2)  (Unable to detect, platform must be declared)
PYBIRD_PLATFORM_AWS_EC2_LINUX2023: str = "aws-ec2-linux2023"  # AWS EC2 (Amazon Linux 2023) (Unable to detect, platform must be declared)
PYBIRD_PLATFORM_WSL: str = "wsl"  # Windows Subsystem for linux
PYBIRD_PLATFORM_PI32: str = "pi32"  # Raspberry Pi 32-bit platform (Unable to detect, platform must be declared)
PYBIRD_PLATFORM_PI64: str = "pi64"  # Raspberry Pi 64-bit platform (Unable to detect, platform must be declared)
PYBIRD_PLATFORM_UNKNOWN: str = "unknown"

PYBIRD_PLATFORM: str = PYBIRD_PLATFORM_LINUX
try:
    TEMP_PLATFORM = os.environ[PYBIRD_PLATFORM_TAG]
    if TEMP_PLATFORM in [PYBIRD_PLATFORM_WINDOWS,
                         PYBIRD_PLATFORM_LINUX,
                         PYBIRD_PLATFORM_MACOS,
                         PYBIRD_PLATFORM_AWS_EC2_LINUX2,
                         PYBIRD_PLATFORM_WSL,
                         PYBIRD_PLATFORM_PI32,
                         PYBIRD_PLATFORM_PI64]:
        PYBIRD_PLATFORM = TEMP_PLATFORM

    else:
        raise PYBIRDPlatformError("PYBIRD_PLATFORM is not supported")
except:
    if sys.platform.startswith(PLATFORM_CHECK_WINDOWS):
        PYBIRD_PLATFORM = PYBIRD_PLATFORM_WINDOWS
    elif sys.platform.startswith(PLATFORM_CHECK_MACOS):
        PYBIRD_PLATFORM = PYBIRD_PLATFORM_MACOS
    elif sys.platform.startswith(PLATFORM_CHECK_LINUX):
        if PLATFORM_CHECK_WSL in uname().release:
            PYBIRD_PLATFORM = PYBIRD_PLATFORM_WSL
        else:
            PYBIRD_PLATFORM = PYBIRD_PLATFORM_LINUX
    else:
        PYBIRD_PLATFORM = PYBIRD_PLATFORM_UNKNOWN

try:
    PYTHON_COMMAND_LINE_STRING: str = os.environ[PYBIRD_PYTHON_TAG]
except:
    PYTHON_COMMAND_LINE_STRING: str = "python3"

# endregion
####################################################################################################

####################################################################################################
# region Keychain Data
AES_KEY_FILE_NAME = "PYBIRD_AES.key"
AES_KEY_SCRAMBLE_LENGTH = 48
AES_BLOCK_SIZE = 16
AES_PASS_LENGTH = 16
AES_ENCODING = "utf-8"

AES_KEY_FILE = os.path.join(PYBIRD_HOME_AES_DIRECTORY, AES_KEY_FILE_NAME)

# endregion
####################################################################################################

####################################################################################################
# region database names
ATLAS_LOG_COLLECTION = "log"

# endregion
####################################################################################################

####################################################################################################
# region OS Specific Settings
if PYBIRD_PLATFORM == PYBIRD_PLATFORM_WINDOWS:  # Windows 10/11
    PLATFORM_HAS_CLI = True
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_LINUX:  # General Linux
    PLATFORM_HAS_CLI = True
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_MACOS:  # MacOS
    PLATFORM_HAS_CLI = True
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_WSL:  # Windows Subsystem for Linux
    PLATFORM_HAS_CLI = True
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = True

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_AWS_EC2_LINUX2:  # AWS EC2 (Amazon Linux 2) Server
    PLATFORM_HAS_CLI = False
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_AWS_EC2_LINUX2023:  # AWS EC2 (Amazon Linux 2) Server
    PLATFORM_HAS_CLI = False
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_PI32:  # Raspberry Pi OS 32 Bit
    PLATFORM_HAS_CLI = False
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

elif PYBIRD_PLATFORM == PYBIRD_PLATFORM_PI64:  # Raspberry Pi OS 64 Bit
    PLATFORM_HAS_CLI = False
    PLATFORM_FORCE_TEST_MODE = False
    PLATFORM_FORCE_DEBUG_MODE = False

# endregion
####################################################################################################
