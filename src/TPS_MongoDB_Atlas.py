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

import TDS_database_atlas


class MongoDB_Atlas:
    def __init__(self, app):
        self.app = app

    def connect_to_database(self, database_name: str):
        """
        Connect to the database
        :param database_name:
        :return:
        """
        if self.app._app_config.plugin_atlas_enabled:
            temp_db = TDS_database_atlas.mongodb_atlas(self.app, database_name)
            if temp_db.valid:
                return temp_db.db
            else:
                self.app.interface.log("Database [" + database_name + "]: Unable to connect", "ERROR")
                return None
        else:
            self.app.interface.log("Atlas Database: Disabled", "ERROR")
            return None
