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

import hashlib
import os
import shutil
import subprocess
import sys
import typing
from dataclasses import dataclass
from datetime import datetime, timezone

import TCS_UIutils
import TCS_config
import TCS_configApp
import TCS_utils
import TCS_variables

LOG_HEADER = "Date,Version,Session ID,Subsystem/App Name, Uptime(s),Step Count,Log Type,Log Message\n"

_h = "\033["
_e = '\033[0;39;49m'

_c = {
    'red': '1',
    'green': '2',
    'orange': '3',
    'blue': '4',
    'pink': '5',
    'teal': '6',
    'white': '7',
    'gray': '9'}

_f = {
    'normal': '0',
    'bold': '1',
    'ulined': '4'}


def msg_color(msg, color='gray', fmt='normal'):
    return _h + _f[fmt] + ';3' + _c[color] + 'm' + msg + _e


@dataclass
class required_app_var:
    """
    NOT USED, provides classes below with a reference of what the app structure is
    """
    name: str = ""
    isApp: bool = False
    _app_config: TCS_configApp._app_config = TCS_configApp._app_config()
    step_count: int = 0


class interface:
    def __init__(self,
                 source_name: str,
                 inDebug: bool = False,
                 ):
        self.version = TCS_utils.version()

        self.sourceName = source_name.upper().replace(" ", "_")
        self.inDebug = inDebug
        self.isApp = False
        self._app: required_app_var = required_app_var()
        self._config = TCS_config.TCS_config()
        self._console_available = self._config.console.show_console
        try:
            self.sessionID, self.startUp = read_state_file()
        except:
            write_state_file(nodeName=self.sourceName)
            self.sessionID, self.startUp = read_state_file()

        self.update_dir()

        self._log_to_db_collection = None

        self.allow_debug = self._config.system.debug_mode or inDebug

    def _add_app(self, app):
        self.isApp = True
        self._app = app
        if self.isApp and self._app._app_config.debug_mode:
            self.allow_debug = True

    def _add_node(self, node):
        self._app = node

    def update_dir(self):
        self.master_log: str = os.path.join(
            TCS_variables.PYBIRD_DATA_LOG_DIRECTORY, "MASTER_LOG.csv")
        if not os.path.exists(self.master_log):
            with open(self.master_log, "w", encoding="utf-8") as f:
                f.write(LOG_HEADER)
            if sys.platform.startswith(TCS_variables.PLATFORM_CHECK_LINUX):
                subprocess.call(['chmod', '666', self.master_log])

        self.app_log: str = os.path.join(
            TCS_variables.PYBIRD_DATA_LOG_DIRECTORY, str("APP_" + self.sourceName + "_LOG.csv"))
        if not os.path.exists(self.app_log):
            with open(self.app_log, "w", encoding="utf-8") as f:
                f.write(LOG_HEADER)
            if sys.platform.startswith(TCS_variables.PLATFORM_CHECK_LINUX):
                subprocess.call(['chmod', '666', self.app_log])

    def _add_collection(self, collection):
        self._log_to_db_collection = collection

    def clear_log(self):
        header_str = "Date,Source Name, Uptime(s),Step Count,Log Type,Log Message\n"
        # confirm clear
        response = TCS_UIutils.userInput("Confirm clear (CONFIRM) Case-Sensitive")
        if response != "CONFIRM":
            print("INVALID CONFIRMATION ABORTING CLEAR")
            return

        log_file = os.listdir(TCS_variables.PYBIRD_DATA_LOG_DIRECTORY)
        for file in log_file:
            try:
                with open(os.path.join(TCS_variables.PYBIRD_DATA_LOG_DIRECTORY, file), "w", encoding="utf-8") as f:
                    f.write(header_str)
            except:
                self.log("Unable to clear " + file, "ERROR")

        for file in log_file:
            self.log(os.path.join(TCS_variables.PYBIRD_DATA_LOG_DIRECTORY, file), "cleared by command")

    def export_log(self):
        log_file = os.listdir(TCS_variables.PYBIRD_DATA_LOG_DIRECTORY)
        date = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.log("FILES TO EXPORT - " + date)
        self.log_list(log_file, "To export")

        dir_out = input("Enter the export location / separated[" + TCS_variables.PYBIRD_LOG_DIRECTORY + "]: ")
        if dir_out == "":
            dir_out = TCS_variables.PYBIRD_LOG_DIRECTORY
        else:
            temp = dir_out.split("/")
            dir_out = os.path.join("/", *temp)

        for file in log_file:
            shutil.copyfile(os.path.join(TCS_variables.PYBIRD_DATA_LOG_DIRECTORY, file),
                            os.path.join(TCS_variables.PYBIRD_LOG_DIRECTORY, date + "_" + file))
            print("EXPORT TO:", TCS_variables.PYBIRD_LOG_DIRECTORY + "/" + date + "_" + file)

    def export_and_clear(self):
        self.export_log()
        self.clear_log()

    ################################################################################################
    # region Standard Logging Methods

    def console(self, in_string: str, logType: str = "MSG") -> None:
        """
        Log a message to console
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None
        """
        con_msg, file_msg = self._build_message(str(in_string), logType=logType)
        self._to_console(con_msg, logType)

    def log(self, in_string: str, logType: str = "MSG") -> None:
        """
        log message to:
            console
            local log
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None       
        """
        con_msg, file_msg = self._build_message(str(in_string), logType=logType)
        self._to_console(con_msg, logType)
        self._log_to_file(file_msg)

    def log_db(self, in_string: str, logType: str = "MSG") -> None:
        """
        log message to:
            console
            local log
            database

        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None       
        """
        logType = self._add_db_type(logType)
        con_msg, file_msg = self._build_message(str(in_string), logType=logType)
        self._to_console(con_msg, logType)
        self._log_to_file(file_msg)
        self._log_to_db(in_string, logType)

    def log_list(self, in_list: list, logType: str = "MSG") -> None:
        """
        log list
        :param in_list: list to be logged
        :param logType: type of log to be logged
        :return: None
        
        Example:
            log_list([1,2,3,4,5,6,7,8,9,10], logType="MSG")
        """
        num_items = len(in_list)
        for i in range(num_items):
            msg = self._get_line_num(i + 1, num_items)
            msg += str(in_list[i])
            con_msg, file_msg = self._build_message(msg, logType=logType)
            self._to_console(con_msg, logType)
            self._log_to_file(file_msg)

    def log_delimiter(self, in_string: str,
                      logType: str = "MSG",
                      delimiter: str = ",",
                      removeBlanks: bool = False) -> None:
        """
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :param delimiter: delimiter to split string
        :param removeBlanks: remove blank lines
        :return: None
        
        Example:
            log_delimiter("1,2,3,4,5,6,7,8,9,10", delimiter=",", removeBlanks=True)
            log_delimiter("1,2,3,4,5,6,7,8,9,10", delimiter=",", removeBlanks=False)
        """
        msgs = str(in_string).split(delimiter)
        if removeBlanks:
            new_msgs = []
            for line in msgs:
                if line != "":
                    new_msgs.append(line)
            msgs = new_msgs

        num_lines = len(msgs)
        for i in range(num_lines):
            msg = self._get_line_num(i + 1, num_lines)
            msg += msgs[i].strip()
            con_msg, file_msg = self._build_message(msg, logType=logType)
            self._to_console(con_msg, logType)
            self._log_to_file(file_msg)

    def log_multiline(self, in_string: str, logType: str = "MSG") -> None:
        """
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None
        """
        self.log_delimiter(in_string=in_string, logType=logType, delimiter="\n")

    def log_dict(self, in_dict: dict, logType: str = "MSG") -> None:
        """
        :param in_dict: dictionary to be logged
        :param logType: type of log to be logged
        :return: None
        
        """
        length = self._dict_length(in_dict=in_dict) + 2
        msg = self._get_line_num(1, length) + "{"
        self.log(msg, logType=logType)

        self._log_dict(in_dict=in_dict, logType=logType, indent=0, total_items=length, in_item_number=2)

        msg = self._get_line_num(length, length) + "}"
        self.log(msg, logType=logType)

    # endregion
    ################################################################################################
    ################################################################################################
    # region DEBUG Logging Methods
    def dlog(self, in_string: str, logType: str = "MSG") -> None:
        """
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None
        """
        if self.allow_debug:
            logType = self._add_debug_type(logType)
            self.log(in_string, logType=logType)

    def dlog_db(self, in_string: str, logType: str = "MSG") -> None:
        """
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None
        """
        if self.allow_debug:
            logType = self._add_debug_type(logType)
            self.log_db(in_string=in_string, logType=logType)

    def dlog_list(self, in_list, logType: str = "MSG") -> None:
        """
        :param in_list: list to be logged
        :param logType: type of log to be logged
        :return: None
        """
        if self.allow_debug:
            logType = self._add_debug_type(logType)
            self.log_list(in_list=in_list, logType=logType)

    def dlog_delimeter(self,
                       in_string: str,
                       logType: str = "MSG",
                       delimiter: str = ",",
                       removeBlanks: bool = False) -> None:
        """
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :param delimiter: delimiter to use
        :param removeBlanks: remove blank lines
        :return: None
        """
        if self.allow_debug:
            logType = self._add_debug_type(logType)
            self.log_delimiter(in_string=in_string,
                               logType=logType,
                               delimiter=delimiter,
                               removeBlanks=removeBlanks)

    def dlog_multiline(self, in_string: str, logType: str = "MSG") -> None:
        """
        :param in_string: string to be logged
        :param logType: type of log to be logged
        :return: None
        """
        if self.allow_debug:
            logType = self._add_debug_type(logType)
            self.log_multiline(in_string, logType=logType)

    def dlog_dict(self, in_dict: dict, logType: str = "MSG") -> None:
        """
        :param in_dict: dictionary to be logged
        :param logType: type of log to be logged
        :return: None
        """
        if self.allow_debug:
            logType = self._add_debug_type(logType)
            self.log_dict(in_dict=in_dict, logType=logType)

    # endregion
    ################################################################################################

    ################################################################################################
    # Log
    def _to_console(self, msg: str, msgType="") -> None:
        """
        :param msg: message to be logged
        :return: None
        """
        if msgType != "":
            if msgType.upper() == "ERROR":
                msg = msg_color(msg, color="red", fmt="bold")
            elif msgType.upper() == "WARNING":
                msg = msg_color(msg, color="orange", fmt="bold")
            elif msgType.upper() == "STEP ERROR":
                msg = msg_color(msg, color="orange", fmt="bold")
            elif "EXIT" in msgType.upper():
                msg = msg_color(msg, color="red", fmt="bold")

        if self._console_available and self._config.platform.has_cli:
            print(msg)
        elif self._config.console.show_console:
            print(msg)
        elif self._config.system.test_mode:
            print(msg)

    def _log_to_file(self, msg: str) -> None:
        """
        :param msg: message to be logged
        :return: None
        """
        try:
            with open(self.master_log, "a", encoding="utf-8") as f:
                f.write(msg)
                f.write("\n")
        except Exception as e:
            raise TCS_variables.PYBIRDIOError("_log_to_file error on primary method only (MASTER LOG)")

        try:
            with open(self.app_log, "a", encoding="utf-8") as f:
                f.write(msg)
                f.write("\n")
        except Exception as e:
            raise TCS_variables.PYBIRDIOError("_log_to_file error on primary method only (APP LOG)")

    def _log_to_db(self, msg: str, type: str) -> None:
        """
        :param msg: message to be logged
        :param type: type of log to be logged
        :return: None
        """
        packet = {
            'app_name': self.sourceName,
            'date': datetime.now(timezone.utc),
            'uptime': self.get_uptime(),
            'step_count': self.get_stepCount(),
            'log_type': type.upper(),
            'message': msg
        }
        if self._log_to_db_collection != None:
            self._log_to_db_collection.insert_one(packet)
        else:
            self.log("_log_to_db: No collection to log to (DB LOG)", "ERROR")

    def _log_dict(self, in_dict: dict, logType: str = "MSG", indent: int = 0, total_items: int = 0,
                  in_item_number: int = 1, nested: bool = False) -> int:
        """
        log dict
        :param in_dict: dictionary to be logged
        :param logType: type of log to be logged
        :param indent: number of indents to be added
        :param total_items: total number of items in dictionary
        :param in_item_number: number of item being logged
        :param nested: is this a nested dictionary
        :return: number of items logged
        """
        num = in_item_number
        for key, value in in_dict.items():
            if isinstance(value, dict):
                msg = self._get_line_num(num, total_items)
                for i in range(indent):
                    msg += "    "
                msg += str(key) + " : {"

                self.log(msg, logType=logType)
                num += 1
                num = self._log_dict(in_dict=value, logType=logType, indent=indent + 1, total_items=total_items,
                                     in_item_number=num, nested=True)
            else:
                msg = self._get_line_num(num, total_items)
                for i in range(indent):
                    msg += "    "
                msg += str(key) + " : " + str(value)
                self.log(msg, logType=logType)
                num += 1
        if nested:
            msg = self._get_line_num(num, total_items)
            for i in range(indent):
                msg += "    "
            msg += "}"
            self.log(msg, logType=logType)
            num += 1
        return num

    ################################################################################################
    # region Private Methods - Logging Methods

    def _add_debug_type(self, message_type: str) -> str:
        """
        :param message_type: type of message to be logged
        :return: message type with DEBUG appended
        """
        return "DEBUG " + message_type.upper()

    def _add_db_type(self, message_type: str) -> str:
        """
        :param message_type: type of message to be logged
        :return: message type with DB appended
        """
        return message_type.upper() + " DB"

    def _dict_length(self, in_dict: dict) -> int:
        """
        :param in_dict: dictionary to be counted
        :return: length of dictionary
        """
        length = 0
        for key, value in in_dict.items():
            if isinstance(value, dict):
                length += 2
                length += self._dict_length(value)
            else:
                length += 1
        return length

    def get_stepCount(self) -> typing.Union[int, None]:
        """
        :return: step count
        """
        if self.isApp:
            return self._app.step_count
        else:
            return None

    def get_uptime(self) -> float:
        """
        :return: uptime in seconds
        """
        return datetime.now(timezone.utc).timestamp() - self.startUp

    def _buildHeader_file(self) -> str:
        """
        :return: string to be logged to file
        """
        header = ""
        header += datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        header += "," + str(self.version)
        header += "," + self.sessionID
        header += "," + self.sourceName
        uptime = str(self.get_uptime())
        if len(str(uptime)) > 10:
            uptime = uptime[:8]

        header += "," + uptime
        header += "," + str(self.get_stepCount())
        header += ","

        return header

    def _buildHeader_con(self) -> str:
        """
        :return: string to be logged to console
        """
        header = "["
        header += datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        header += "] [" + self.sourceName
        header += "] "

        return header

    def _build_message(self, in_string: str, logType: str = "MSG") -> typing.Tuple[str, str]:
        """
        :param in_string: string to be logged
        :param logType: type of log
        :return: tuple of string to be logged to console and file
        
        """
        msg_con = self._buildHeader_con()
        msg_con += "[" + str(logType).upper() + "] -> "
        msg_con += str(in_string)

        msg_file = self._buildHeader_file()
        msg_file += str(logType).upper() + ","
        msg_file += str(in_string.replace(",", "|"))
        return msg_con, msg_file

    def _get_line_num(self, line_num: int, total_lines: int) -> str:
        """
        :param line_num: current line number
        :param total_lines: total lines 
        :return: string of line number with total lines
        
        """
        return "[" + str(line_num) + "/" + str(total_lines) + "] "

    # endregion 
    ################################################################################################
    ################################################################################################


class app_interface(interface):
    def __init__(self, inApp: required_app_var):
        inDebug = (inApp.isApp and inApp._app_config.debug_mode)
        super().__init__(inApp.name, inDebug)
        self._add_app(inApp)

    def updateName(self):
        self.sourceName = self._app.name

    def get_stepCount(self):
        if self.isApp:
            return self._app.step_count
        else:
            return None


class node_interface(interface):
    def __init__(self, inNode: required_app_var):
        super().__init__(inNode.name)
        self._add_node(inNode)

    def updateName(self):
        self.sourceName = self._app.name

    def get_stepCount(self):
        if self.isApp:
            return self._app.step_count
        else:
            return None


def write_state_file(nodeName):
    # hash: nodeName + PID + start up time
    # session ID = nodeName+hash[:6]

    # file lines
    # node name
    # start time
    # pid
    # full hash
    # session ID
    pid = str(os.getpid())
    date = str(datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f%z"))
    s_str: str = nodeName + pid + date
    b_str = s_str.encode()
    my_hash = hashlib.md5(b_str).hexdigest()
    sessionID = nodeName + "-" + my_hash[:8]

    file_path = os.path.join(TCS_variables.PYBIRD_DATA_SESSION_DIRECTORY, pid)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file = os.path.join(file_path, "session_info.id")

    with open(file, "w") as f:
        f.write(nodeName + "\n")
        f.write(date + "\n")
        f.write(pid + "\n")
        f.write(s_str + "\n")
        f.write(my_hash + "\n")
        f.write(sessionID)


def read_state_file():
    pid = str(os.getpid())
    file_path = os.path.join(TCS_variables.PYBIRD_DATA_SESSION_DIRECTORY, pid)
    file = os.path.join(file_path, "session_info.id")
    with open(file, "r") as f:
        lines = f.readlines()
        nodeName = lines[0].strip()
        startTime = lines[1].strip()
        pid = lines[2].strip()
        combined = lines[3].strip()
        full_hash = lines[4].strip()
        sessionID = lines[5].strip()

    start = datetime.strptime(startTime, "%Y%m%d%H%M%S%f%z").timestamp()
    return sessionID, start


if __name__ == "__main__":
    write_state_file("N000")
    read_state_file()
    inter = interface(source_name="INTERFACE_TESTING")
    inter.log("test1", "error")
    inter.log("test2", "warning")
    inter.log("test3", "test")

    # # inter.log_delimiter("test,,test2,,test3",removeBlanks=True)
    # test_dict = {"test": "test",
    #              "test2": "test2",
    #              "test3": "test3",
    #              "test4": {"te,st4a": "test4a"},
    #              "test5": {"test5a": "test5a",
    #                        "test5b": "test5b"},
    #             "test6": {"test6a": "test6a",
    #                       "test6b": "test6b",
    #                       "test6c": {
    #                           "test6ca": "test6ca",
    #                           "test6cb": "test6cb"
    #                       }}}
    # inter.log_dict(test_dict)
