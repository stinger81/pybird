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

from dataclasses import dataclass



@dataclass
class PYBIRD_VER:
    """
    PYBIRD version
    """
    MAJOR = 0
    MINOR = 9
    PATCH = 0
    BUILD = 3
    PRE: bool = True
    RC: bool = False
    BETA: bool = False
    ALPHA: bool = True
    DEV: bool = False


@dataclass
class PYBIRD_ENV:
    """
    PYBIRD environment variables
    """
    # Must also be changed in TBS_bootloader_vars.py
    TAG: str = 'PYBIRD'
    REMOTE_DIR_TAG = 'PYBIRDRemoteDir'
    PLATFORM_TAG = 'PYBIRDPlatform'
    PYTHON_TAG = 'PYBIRDPython'
@dataclass
class SYS_ARG:
    """
    System arguments
    """
    # info
    HELP = ['--help'] # will print the help information and then exit
    VERSION = ['--version'] # will print the version information and then exit

    # run declarations
    HOME = ['-H', '--home'] # a flag for listing where the home directory is
    NODE = ['-n', '--node'] # a flag for running a specific node
    APP = ['-a', '--app'] # a flag for running a specific app

    # standard modes
    BOOT = ['-b', '--boot'] # a flag for the system starting from a service on boot
    DEBUG = ['-d', '--debug'] # a flag for running the system in debug mode
    OPERATIONS = ['-o', '--operations'] # a flag for running the system in operations mode (Override debug and test to f)
    HEADLESS = ['-h', '--headless'] # a flag for running the system in headless mode

    # development modes
    DEV = ['--dev'] # a flag for running the system in dev mode
    TEST = ['-t', '--test'] # a flag for running the system in test mode
    RAISE = ['--raise'] # a flag for raising an exception

    _help_msg = """
    Information:
    --help           Print this help message and exit
    --version        Print version information and exit
    
    Run Declarations:
    -H|--home        Set the home directory
    -n|--node        Run a specific node
    -a|--app         Run a specific app
    
    Standard Modes:
    -b|--boot        Declare that the system is starting from a service on boot
    -d|--debug       Run the system in debug mode
    -o|--operations  Run the system in operations mode (Override debug and test to false)
    -h|--headless    Run the system in headless mode
    
    Development Modes:
    --dev            Run the system in dev mode
    -t|--test        Run the system in test mode
    --raise          Raise all exceptions so that error tracebacks are printed
    """






@dataclass
class SESSION:
    """
    Session info
    """
    DATETIME_FORMAT = '%Y%m%d%H%M%S%f%z'
    # FILE_EXTENSION = '.sessionID'
    UNIQUE_ID_LENGTH = 8  # MD5 hash, max length of 32


@dataclass
class DIRECTORY_NAME:
    """
    Directory names
    """
    HOME_DATA = '.pybird'
    SRC = 'src'
    LOG = 'log'
    CONFIG = 'config'
    APP_LOCAL = 'PYBIRD_APPS'
    DATA = 'data'
    SESSION = 'session'
    APPDATA = 'appdata'
    ADD_CRED = "add_cred"
    HOME_DATA_AES = '.aes'
    HOME_DATA_APP = '.app'
    HOME_DATA_ATLAS = '.atlas'
    HOME_DATA_X = '.x'
    HOME_DATA_GENERAL = '.general'


@dataclass
class FILE_EXTENSIONS:
    PY = '.py'
    JSON = '.json'
    TXT = '.txt'
    CSV = '.csv'
    LOG = '.log'
    SESSION = '.sessionID'
    KEY_AES = '.aes.key'
    KEY_ATLAS = '.atlas.key'
    KEY_X = '.x.key'
    KEY_GENERAL = '.general.key'
    UPLOAD_ATLAS = '.atlas.json'
    UPLOAD_X = '.x.json'
    UPLOAD_GENERAL = '.gen.txt'
    SESSION_ID = '.sessionID'
    NODE_CONFIG = '_NODE_CONFIG.csv'


@dataclass
class PLATFORM_CHECK:
    WINDOWS: str = "win"
    LINUX: str = "linux"
    MACOS: str = "darwin"
    WSL: str = "microsoft-standard"


@dataclass
class PLATFORM:
    WINDOWS: str = 'windows'  # windows 10/11
    LINUX: str = 'linux'  # general linux
    MACOS: str = "macos"  # MacOS
    AWS_EC2_LINUX2: str = "aws-ec2-linux2"  # AWS EC2 (Amazon Linux 2)  (Unable to detect, platform must be declared)
    AWS_EC2_LINUX2023: str = "aws-ec2-linux2023"  # AWS EC2 (Amazon Linux 2023) (Unable to detect, platform must be declared)
    WSL: str = "wsl"  # Windows Subsystem for linux
    PI32: str = "pi32"  # Raspberry Pi 32-bit platform (Unable to detect, platform must be declared)
    PI64: str = "pi64"  # Raspberry Pi 64-bit platform (Unable to detect, platform must be declared)
    UNKNOWN: str = "unknown"


@dataclass
class AES:
    """
    AES encryption
    """
    KEY_FILE_NAME = "PYBIRD_AES.key"
    KEY_SCRAMBLE_LENGTH = 48
    BLOCK_SIZE = 16
    PASS_LENGTH = 16
    ENCODING = "utf-8"


@dataclass
class DEFAULT:
    """
    Default values
    """
    COMMAND_LINE_KEY = 'python3'


@dataclass
class ATLAS:
    LOG_COLLECTION = "log"


HELP = """
    PYBIRD
    A python based server for app based systems

    """ + SYS_ARG._help_msg

