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

import TPS_MongoDB_Atlas
import TPS_Twitter
import TPS_dataStruct
import TPS_progressBar


class Plugins:
    """
    This class is a collection of all plugins that are used in the TAS_app
    Categories:
    - SocialMedia
    - DataBase
    - Utils
    """

    class SocialMedia:
        """
        This class is a collection of all SocialMedia plugins
        - Twitter
        """

        class Twitter(TPS_Twitter.Twitter):
            def __init__(self, app):
                super().__init__(app)

    class DataBase:
        """
        This class is a collection of all DataBase plugins
        - MongoDB Atlas
        """

        class MongoDB(TPS_MongoDB_Atlas.MongoDB_Atlas):
            def __init__(self, app):
                super().__init__(app)

    class Utils:
        """
        This class is a collection of all Utils plugins
        - ProgressBar
        - Queue
        - Stack
        - PriorityQueue
        """

        class ProgressBar(TPS_progressBar.ProgressBar):
            def __init__(self):
                super().__init__()

        class Queue(TPS_dataStruct.queue):
            def __init__(self):
                super().__init__()

        class Stack(TPS_dataStruct.stack):
            def __init__(self):
                super().__init__()

        class PriorityQueue(TPS_dataStruct.PriorityQueue):
            def __init__(self):
                super().__init__()


if __name__ == "__main__":
    queue = Plugins.Utils.Queue()
    queue.push(1)
    print(queue)
