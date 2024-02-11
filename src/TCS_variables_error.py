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

####################################################################################################
# region Exceptions


class PYBIRDError(Exception):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDIOError(IOError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDOSError(OSError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDPlatformError(OSError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDKeyError(KeyError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDValueError(ValueError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDIndexError(IndexError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDTypeError(TypeError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDNotImplementedError(NotImplementedError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDAESkeyERROR(PYBIRDError):
    """
    Exception raised while working with PYBIRD
    """
    pass


class PYBIRDAPPkeyERROR(PYBIRDError):
    """
    Exception raised while working with PYBIRD
    """
    pass
# endregion
####################################################################################################
