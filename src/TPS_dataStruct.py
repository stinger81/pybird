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
import heapq


class stack:
    """
    stack FILO
    - push() - adds an element into the stack
    - pop() - removes an element from the stack
    - top() - returns the element at the top of the stack
    - size() - returns the number of elements in the stack
    - empty() - returns true if the stack is empty
    """

    def __init__(self) -> None:
        self.data = []

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def push(self, in_object) -> None:
        """
        Inserts an object to the top of the stack
        :param in_object:
        :return: 
        """
        self.data.append(in_object)

    def pop(self):
        """
        Removes the top element from the stack
        Returns None if the stack is empty
        :return: 
        """
        if self.size() == 0:
            return None
        return self.data.pop()

    def top(self):
        """
        returns the top element of the stack
        :return: 
        """
        if self.size() == 0:
            return None
        return self.data[-1]

    def size(self):
        """
        returns the number of elements in the stack
        :return: 
        """
        return len(self.data)

    def empty(self):
        """
        returns true if the stack is empty
        :return: 
        """
        if self.size() == 0:
            return True
        return False


class queue:
    """
    queue FIFO
    - push() - inserts an element at the back of the queue
    - pop() - removes an element from the front of the queue
    - front() - returns the first element of the queue
    - back() - returns the last element of the queue
    - size() - returns the number of elements in the queue
    - empty() - returns true if the queue is empty
    """

    def __init__(self) -> None:
        self.data = []

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def push(self, in_value):
        """
        Inserts an object to the back of the queue
        :param in_value: 
        :return: 
        """
        self.data.append(in_value)

    def pop(self):
        """
        Removes the first element from the queue
        Returns None if the queue is empty
        :return: 
        """
        if self.size() == 0:
            return None

        return self.data.pop(0)

    def front(self):
        """
        returns the first element of the queue
        :return: 
        """
        if self.size() == 0:
            return None
        return self.data[0]

    def back(self):
        """
        returns the last element of the queue
        :return: 
        """
        if self.size() == 0:
            return None
        return self.data[-1]

    def size(self):
        """
        returns the number of elements in the queue
        :return: 
        """
        return len(self.data)

    def empty(self):
        """
        returns true if the queue is empty
        :return: 
        """
        if self.size() == 0:
            return True
        return False


class PriorityQueue:
    """
    PriorityQueue
    - push() - adds an element into the queue
    - pop() - removes an element from the queue
    - isEmpty() - returns true if the queue is empty
    - update() - updates the priority of an element
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        """
        Adds an element to the queue
        :param item:
        :param priority:
        :return:
        """
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        """
        Removes an element from the queue
        :return:
        """
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        """
        returns true if the queue is empty
        :return:
        """
        return len(self.heap) == 0

    def update(self, item, priority):
        """
        Updates the priority of an element
        :param item:
        :param priority:
        :return:
        """

        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
