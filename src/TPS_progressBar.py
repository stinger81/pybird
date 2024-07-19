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
import TCS_utils


class ProgressBar:
    """
    Generates a progress bar
    """

    def __init__(self):

        self.version = TCS_utils.version()

        self.barlength: int = 25  # Number of fill blocks in the bar
        self.barend_front = "|"
        self.barend_back = "|"

        self.percent_front = "("
        self.percent_back = ")"

        self.showPercentage = True
        self.decimalPlaces = 2
        self.partialBlock = False
        self._warning = True
        self.barend = True

        self.BLOCK_8_8 = "\u2588"
        self.BLOCK_7_8 = "\u2587"
        self.BLOCK_6_8 = "\u2586"
        self.BLOCK_5_8 = "\u2585"
        self.BLOCK_4_8 = "\u2584"
        self.BLOCK_3_8 = "\u2583"
        self.BLOCK_2_8 = "\u2582"
        self.BLOCK_1_8 = "\u2581"
        self.BLOCK_0_8 = "\u2581"

        self.WARNING_SYMBOL = "\u26A0 "

        self._warning_len = 2

    def enable_barend(self):
        """
        enables barend
        """
        self.barend = True

    def disable_barend(self):
        """
        disables barend
        """
        self.barend = False

    def enable_full_blocks(self):
        """
        enables full blocks
        """

        self.partialBlock = False
        self.BLOCK_0_8 = "\u2591"

    def enable_partial_blocks(self):
        """
        enables partial blocks
        """
        self.partialBlock = True
        self.BLOCK_0_8 = "\u2581"

    def enable_warning(self):
        """
        enables warning
        """
        self._warning = True

    def disable_warning(self):
        """
        disables warning
        """
        self._warning = False

    def set_percentage(self, show: bool):
        """
        Sets the percentage
        :param show: bool
        :return: None
        """
        self.showPercentage = show

    def set_decimal_places(self, places: int):
        """
        Sets the decimal places
        :param places: int
        :return: None
        """

        self.decimalPlaces = places

    def set_bar_length(self, length: int):
        """
        Sets the bar length
        :param length: int
        :return: None
        """

        self.barlength = length

    def set_warning_len(self, length: int):
        """
        Sets the warning length
        :param length: int
        :return: None
        """

        self._warning_len = length

    def set_barend(self, end: str):
        """
        Sets the barend
        :param end: str
        :return: None
        """

        self.barend_front = end
        self.barend_back = end

    def get_percent(self, progress: int, length: int) -> float:
        """
        Returns the percentage of the progress
        :param progress: int
        :param length: int
        :return: float
        """
        return progress / length

    def _updateBlockList(self):
        """
        updates the block list
        """
        self.blocks_list = [self.BLOCK_0_8,
                            self.BLOCK_1_8,
                            self.BLOCK_2_8,
                            self.BLOCK_3_8,
                            self.BLOCK_4_8,
                            self.BLOCK_5_8,
                            self.BLOCK_6_8,
                            self.BLOCK_7_8,
                            self.BLOCK_8_8]

    def get_bar(self, percent: float):
        """
        Creates a progress bar with a percentage
        :param percent: float
        :return: str
        """
        self._updateBlockList()
        # Calculate the number of blocks to fill
        total_blocks = percent * self.barlength
        blocks = int(percent * self.barlength)
        partial = int((total_blocks - blocks) * 8)
        # Create the bar
        if self.barend:
            bar = self.barend_front
        else:
            bar = ""
        for i in range(blocks):
            bar += self.BLOCK_8_8
        if self.partialBlock:
            if blocks != self.barlength:
                bar += self.blocks_list[partial]
                blocks += 1
        for i in range(self.barlength - blocks):
            bar += self.BLOCK_0_8
        if self.barend:
            bar += self.barend_back
        # Add the percentage
        if self.showPercentage:
            bar += " "
            bar += self.percent_front
            bar += f"{percent:.{self.decimalPlaces}%}"
            bar += self.percent_back
            if self._warning and percent > 1:
                for self.i in range(self._warning_len):
                    bar += self.WARNING_SYMBOL + ""
        # Return the bar
        return bar


if __name__ == "__main__":
    n = 1
    bar = ProgressBar()
    bar.enable_partial_blocks()
    bar.set_bar_length(25)
    bar.set_decimal_places(2)
    bar.disable_warning()
    bar.enable_warning()
    for i in range(0, 105):
        print(bar.get_bar(bar.get_percent(i, 100)))
