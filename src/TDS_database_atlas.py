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

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import TCS_utils
import TKS_keychain


# https://stackoverflow.com/questions/4421207/how-to-get-the-last-n-records-in-mongodb
class mongodb_atlas:
    def __init__(self, app, DB_name) -> None:

        self.version = TCS_utils.version()

        self._app = app

        keychain = TKS_keychain.keychain()
        self.valid = True
        try:
            keys = keychain.load_atlas_keys(app.name, DB_name)

            self.app_name = keys[0]
            self.uri = keys[1]
            self.server_api = keys[2]
            self.database_name = keys[3]

            self.client = MongoClient(self.uri, server_api=ServerApi(self.server_api))

            try:
                self.client.admin.command('ping')
                self._app.interface.dlog("Connected to MongoDB Atlas")
            except Exception as e:
                self._app.interface.log("Could not connect to MongoDB Atlas [" + self.database_name + "]")
                e_mod = str(e).split("\n")
                for i in e_mod:
                    self._app.interface.log(i)

            self.db = self.client.get_database(self.database_name)
        except:
            self._app.interface.log(str("Unable to load atlas credential for " + DB_name), "ERROR")
            self.valid = False
        # delete variables after use (Security Risk if left)
        try:
            del keychain
        except:
            pass
        try:
            del keys
        except:
            pass
        try:
            del self.uri
        except:
            pass
        try:
            del self.server_api
        except:
            pass
        try:
            del self.database_name
        except:
            pass

    def join_collection(self, collection_name):
        """
        Join a collection
        :param collection_name:
        :return:
        """
        return self.db.get_collection(collection_name)

    def database_status(self):
        """
        Get the database status
        :return:
        """
        return self.db.command({"dbStats": 1})


if __name__ == "__main__":
    pass
