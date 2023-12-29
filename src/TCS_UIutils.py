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

import typing


class userInterface:
    def __init__(self, title: str, message: str = ""):
        self.title = title
        self.message = message
        self.input = None
        self.default: int = -1
        self.options = []
        self.hasQuit = False

    def addOption(self, command: str, description: str, functionToCall=None, isDefault: bool = False,
                  requireConfirmation: bool = False, confirmationCode="CONFIRM"):
        if isDefault:
            self.default = len(self.options)
        self.options.append((command, description, functionToCall, requireConfirmation, confirmationCode))

    def addHeader(self, header: str):
        self.options.append(("header", header, None, False, ""))

    def addQuit(self, isDefault: bool = False):
        self.hasQuit = True
        self.addOption("q", "Quit", None, isDefault)

    def _generateUI(self):
        print()
        print(self.title)
        if self.message != "":
            print(self.message)
        for choice in self.options:
            if choice[0] == "header":
                print()
                print(choice[1])
            elif self.hasQuit and choice[0] == "q":
                pass
            else:
                print(choice[0], " - ", choice[1])

        if self.hasQuit:
            print()
            print("q - Quit")

    def getUserResponse(self):
        """
        returns the user's response as a tuple of the form (command, functionToCall)
        """
        default = "[]"
        if self.default >= 0:
            default = "[" + self.options[self.default][0] + "]"
        self._generateUI()

        while True:
            userResponse = input("Select an option " + default + ":")
            if userResponse == "":
                userResponse = self.options[self.default][0]
            for choice in self.options:
                if self.hasQuit and userResponse == "q":
                    exit(0)
                if choice[0] == userResponse:
                    if choice[3]:
                        code = input("Please type the following confirmation code to confirm (" + choice[4] + "): ")
                        if code == choice[4]:
                            return choice
                        else:
                            continue
                    else:
                        return choice
            self._generateUI()
            print("Invalid option - Please review the options")

    def run(self):
        while True:
            response = self.getUserResponse()
            try:
                response[2]()
            except Exception as e:
                print(e)
                print("Error in function")


def userInput(message: str, default: str = ""):
    msg = message + " [" + default + "]: "
    response = input(msg)
    if response == "":
        return default
    else:
        return response


def userInputValidate(message: str, default: str = "", validList: typing.List[str] = []):
    modList = validList
    if default != "":
        if default not in modList:
            modList.append(default)

    while True:
        response = userInput(message=message,
                             default=default)
        if response in validList:
            return response
        else:
            print("Invalid Response: Please review the list and try again")
