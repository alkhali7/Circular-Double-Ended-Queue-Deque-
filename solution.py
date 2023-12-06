"""
Project 5: Deque
Shams Alkhalidy
"""

import gc
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# COMMENT OUT THIS LINE (and `plot_speed`) if you don't want matplotlib
from matplotlib import pyplot as plt

T = TypeVar('T')
CDLLNode = type('CDLLNode')

class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = None if not data else self.size + front - 1
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[index + front] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = [f"CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque - this is the number of items currently in the circular deque, and will not necessarily be equal to the capacity
        This is a magic method and can be called with len(object_to_measure)
        Time complexity: O(1), Space complexity: O(1)
        Returns: int representing length of the circular deque
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty
        Time complexity: O(1), Space complexity: O(1)
        Returns: True if empty, False otherwise
        """
        if self.size == 0:
            return True
        return False

    def front_element(self) -> T:
        """
        Returns the first element in the circular deque
        Time complexity: O(1), Space Complexity: O(1)
        Returns: the first element if it exists, otherwise None
        """
        if self.front is not None:
            return self.queue[self.front]
        return None

    def back_element(self) -> T:
        """
        Returns the last element in the circular deque
        Time complexity: O(1), Space complexity: O(1)
        Returns: the last element if it exists, otherwise None
        """
        if self.back is not None:
            return self.queue[self.back]
        return None

    def grow(self) -> None:
        """
        Doubles the capacity of CD by creating a new underlying python list with double the capacity of
        the old one and copies the values over from the current list.
        The new copied list will be 'unrolled' s.t. the front element will be at index 0 and
         the tail element will be at index [size - 1].
        Time complexity: O(n) img * Space complexity: O(n)
        Returns: None
        """
        old = self.queue    # make a copy of old queue
        self.capacity = 2 * self.capacity       # double cap
        self.queue = [None] * self.capacity     # make a new queue with the doubled capacity

        # old queue front index
        walk = self.front
        for i in range(self.size):      # only consider existing elements
            self.queue[i] = old[walk]   # copy the first element from last queue to new queue at index 0
            walk = (1+walk) % len(old)  # use old size as modulo, this moves to the next index in old queue
        self.front = 0      # set new front to be at beginning of queue
        self.back = self.size - 1

    def shrink(self) -> None:
        """
        Cuts the capacity of the queue in half using the same idea as grow.
        Copy over contents of the old list to a new list with half the capacity.
        The new copied list will be 'unrolled' s.t. the
        front element will be at index 0 and the tail element will be at index [size - 1].
        Will never have a capacity lower than 4, DO NOT shrink when shrinking would result in a capacity <= 4
        Time complexity: O(n), Space complexity: O(n)
        Returns: None
        """
        old = self.queue

        # if self.capacity > 4:
        new_capacity = self.capacity // 2
        if new_capacity < 4:
            new_capacity = 4
        # self.capacity = self.capacity // 2
        self.queue = [None] * new_capacity
        walk = self.front
        for i in range(self.size):
            self.queue[i] = old[walk]
            walk = (1+walk) % len(old)
        self.front = 0
        self.back = self.size - 1
        self.capacity = new_capacity

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Add a value to either the front or back of the circular deque based off the parameter front
        if front is true, add the value to the front. Otherwise, add it to the back
        param value: T: value to add into the circular deque
        param value front: where to add value T
        Time complexity: O(1)*, Space complexity: O(1)*
        Returns: None
        """
        if front:
            # add to front of queue
            # if there isn't a front yet, set front and back = 0
            if self.front is None:
                self.front = 0
                self.back = 0
            else:
                # calculate new front index to be the index before front
                self.front = (self.front - 1) % self.capacity
            self.queue[self.front] = value
        # adding to end of queue
        else:
            if self.back is None:
                self.front = 0
                self.back = 0
            else:
                self.back = (self.back+1) % self.capacity  # new back index
            self.queue[self.back] = value
        self.size += 1

        # resize if capacity has been reached, Call grow() if the size of the list has reached capacity
        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Remove an item from the queue
        Removes the front item by default, remove the back item if False is passed in

        param front: Whether to remove the front or back item from the dequeue
        Hint: You shouldn't delete the value from the dequeue (by setting it to None) as that
        spot will merely be overwritten when you enqueue on that spot so it's more
        efficient to only adjust the back/front pointer instead.
        Time complexity: O(1)*, Space complexity: O(1)*
        Returns: removed item, None if empty
        """
        # if its already empty, then nothing to remove
        if self.is_empty():
            return None
        # remove from front (first item)
        if front:
            removed_item = self.queue[self.front]
            self.front = (self.front+1) % len(self.queue)  # front index is incremented
        else:
            # deleting last value (tail)
            removed_item = self.queue[self.back]
            self.back = (self.back - 1) % len(self.queue)  # back index is decremented

        self.size -= 1
        # Calls shrink() If the current size is less than or equal to 1/4 the current capacity,
        # and 1/2 the current capacity is greater than or equal to 4, halves the capacity.
        if (self.size <= (1/4 * self.capacity)) and (1/2 * self.capacity >= 4):
            self.shrink()
        return removed_item

class CDLLNode:
    """
    Node for the CDLL
    """

    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -> None:
        """
        Creates a CDLL node
        :param val: value stored by the next
        :param next: the next node in the list
        :param prev: the previous node in the list
        :return: None
        """
        self.val = val
        self.next = next
        self.prev = prev

    def __eq__(self, other: CDLLNode) -> bool:
        """
        Compares two CDLLNodes by value
        :param other: The other node
        :return: true if comparison is true, else false
        """
        return self.val == other.val

    def __str__(self) -> str:
        """
        Returns a string representation of the node
        :return: string
        """
        return "<= (" + str(self.val) + ") =>"

    __repr__ = __str__


class CDLL:
    """
    A (C)ircular (D)oubly (L)inked (L)ist
    """

    __slots__ = ['head', 'size']

    def __init__(self) -> None:
        """
        Creates a CDLL
        :return: None
        """
        self.size = 0
        self.head = None

    def __len__(self) -> int:
        """
        :return: the size of the CDLL
        """
        return self.size

    def __eq__(self, other: 'CDLL') -> bool:
        """
        Compares two CDLLs by value
        :param other: the other CDLL
        :return: true if comparison is true, else false
        """
        n1: CDLLNode = self.head
        n2: CDLLNode = other.head
        for _ in range(self.size):
            if n1 != n2:
                return False
            n1, n2 = n1.next, n2.next
        return True

    def __str__(self) -> str:
        """
        :return: a string representation of the CDLL
        """
        n1: CDLLNode = self.head
        joinable: List[str] = []
        while n1 is not self.head:
            joinable.append(str(n1))
            n1 = n1.next
        return ''.join(joinable)

    __repr__ = __str__

    def insert(self, val: T, front: bool = True) -> None:
        """
        inserts a node with value val in the front or back of the CDLL
        Don't forget to keep it circular!!
        param val: T: the value to insert
        param front: bool = True:  whether to insert in the front of the list, or the back.
        Time Complexity: O(1), Space Complexity: O(1)
        return: None
        """
        new_node = CDLLNode(val)
        # if empty, add it
        if self.size == 0:
            self.head = new_node
            new_node.prev = new_node
            new_node.next = new_node
        else:
            if front:
                new_node.next = self.head
                new_node.prev = self.head.prev
                self.head.prev = new_node
                self.head = new_node
                self.head.prev.next = new_node   # making it circular by connecting the previous last node to the new node.
            else:
                # insert to back
                new_node.next = self.head
                new_node.prev = self.head.prev
                # Connect the previous last node to the new node.
                self.head.prev.next = new_node
                self.head.prev = new_node
        self.size += 1

    def remove(self, front: bool = True) -> None:
        """
        removes a node from the CDLL
        Don't forget to keep it circular!!
        If the list is empty, do nothing
        param front: bool = True: whether to remove from the front of the list, or the back
        Time Complexity: O(1)
        Space Complexity: O(1)
        return: None
        """
        if self.size == 0:
            return
        if self.size == 1:
            self.head = None
            self.size -= 1
            return
        if front:
            # remove first element (head) , 3, 2, 1 -- 2,1
            self.head.next.prev = self.head.prev  # setting 2nd element prev pointer
            self.head.prev.next = self.head.next    # adjusting last element to point to 2nd index
            self.head = self.head.next      # 2nd element is the new head
        else:
            # remove last element (tail),  1,2,3  -- 1,2
            self.head.prev.prev.next = self.head   # making element before tail to point to head
            self.head.prev = self.head.prev.prev    # adjusting head's prev pointer to point to element before tail
        self.size -= 1


class CDLLCD:
    """
    (C)ircular (D)oubly (L)inked (L)ist (C)ircular (D)equeue
    This is essentially just an interface for the above
    """

    def __init__(self) -> None:
        """
        Initializes the CDLLCD to an empty CDLL
        :return: None
        """
        self.CDLL: CDLL = CDLL()

    def __eq__(self, other: 'CDLLCD') -> bool:
        """
        Compares two CDLLCDs by value
        :param other: the other CDLLCD
        :return: true if equal, else false
        """
        return self.CDLL == other.CDLL

    def __str__(self) -> str:
        """
        :return: string representation of the CDLLCD
        """
        return str(self.CDLL)

    __repr__ = __str__

    def __len__(self) -> int:
        """
        Returns the length/size of the CDLLCD, and hence the underlying CDLL.
        This is a magic method and can be called with len(object_to_measure)
        Time complexity: O(1)
        Space complexity: O(1)
        Returns: int representing length of the CDLLCD
        """
        return self.CDLL.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the CDLLCD is empty
        Time complexity: O(1)
        Space complexity: O(1)
        Returns: True if empty, False otherwise
        """
        if self.CDLL.size == 0:
            return True
        return False

    def front_element(self) -> T:
        """
        Returns the first element in the CDLLCD
        Time complexity: O(1)
        Space Complexity: O(1)
        Returns: the first element if it exists, otherwise None
        """
        if self.CDLL.head is not None:
            return self.CDLL.head.val   # Access the 'val' attribute of the CDLLNode
        return None

    def back_element(self) -> T:
        """
        Returns the last element in the CDLLCD
        Time complexity: O(1)
        Space complexity: O(1)
        Returns: the last element if it exists, otherwise None
        """
        if self.CDLL.head:
            return self.CDLL.head.prev.val
        return None

    def enqueue(self, val: T, front: bool = True) -> None:
        """
        Adds a value to the CDLLCD
        Must use the insert function of the CDLL class
        param val: T: the value to be added
        param front: bool = True: whether to add to the front or the back of the deque
        Time complexity: O(1)
        Space complexity: O(1)
        return: None
        """
        if front:
            self.CDLL.insert(val, front=True)
        else:
            self.CDLL.insert(val, front=False)

    def dequeue(self, front: bool = True) -> T:
        """
        Removes a value from the deque, returning it
        Must use the remove function of the CDLL class
        param front: bool = True: whether to remove from the front or the back of the deque
        Time complexity: O(1), Space complexity: O(1)
        return: The dequeued element, None if empty
        """
        # empty
        if self.CDLL.size == 0:
            return None

        if front:
            removed = self.CDLL.head.val
            self.CDLL.remove(front=True)
        else:
            removed = self.CDLL.head.prev.val
            self.CDLL.remove(front=False)
        return removed


def plot_speed():
    """
    Compares performance of the CDLLCD and the standard array based deque
    """

    # First we'll test sequences of basic operations

    sizes = [100*i for i in range(0, 200, 5)]

    # (1) Grow large
    grow_avgs_array = []
    grow_avgs_CDLL = []

    for size in sizes:
        grow_avgs_array.append(0)
        grow_avgs_CDLL.append(0)
        data = list(range(size))
        for trial in range(3):

            gc.collect()  # What happens if you remove this? Hint: memory fragmention
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            grow_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            grow_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, grow_avgs_array, color='blue', label='Array')
    plt.plot(sizes, grow_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue and Grow")
    plt.legend(loc='best')
    plt.show()

    # (2) Grow Large then Shrink to zero

    shrink_avgs_array = []
    shrink_avgs_CDLL = []

    for size in sizes:
        shrink_avgs_array.append(0)
        shrink_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            for item in data:
                cd_array.dequeue(not item % 2)
            shrink_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            for item in data:
                cd_DLL.dequeue(not item % 2)
            shrink_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, shrink_avgs_array, color='blue', label='Array')
    plt.plot(sizes, shrink_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue, Grow, Dequeue, Shrink")
    plt.legend(loc='best')
    plt.show()

    # (3) Test with random operations

    random_avgs_array = []
    random_avgs_CDLL = []

    for size in sizes:
        random_avgs_array.append(0)
        random_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            shuffle(data)

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_array.enqueue(item, item % 2)
                else:
                    cd_array.dequeue(item % 2)
            random_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_DLL.enqueue(item, item % 2)
                else:
                    cd_DLL.dequeue(item % 2)
            random_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, random_avgs_array, color='blue', label='Array')
    plt.plot(sizes, random_avgs_CDLL, color='red', label='CDLL')
    plt.title("Operations in Random Order")
    plt.legend(loc='best')
    plt.show()

    def max_len_subarray(data, bound, structure):
        """
        returns the length of the largest subarray of `data` with sum less or eq to than `bound`
        :param data: list of integers to operate on
        :param bound: largest allowable sum
        :param structure: either a CircularDeque or a CDLLCD
        :return: the length
        """
        index, max_len, subarray_sum = 0, 0, 0
        while index < len(data):

            while subarray_sum <= bound and index < len(data):
                structure.enqueue(data[index])
                subarray_sum += data[index]
                index += 1
            max_len = max(max_len, subarray_sum)

            while subarray_sum > bound:
                subarray_sum -= structure.dequeue(False)

        return max_len

    # (4) A common application

    application_avgs_array = []
    application_avgs_CDLL = []

    data = [randint(0, 1) for i in range(5000)]
    window_lengths = list(range(0, 200, 5))

    for length in window_lengths:
        application_avgs_array.append(0)
        application_avgs_CDLL.append(0)

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            start = default_timer()
            max_len_subarray(data, length, cd_array)
            application_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            max_len_subarray(data, length, cd_DLL)
            application_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(window_lengths, application_avgs_array,
             color='blue', label='Array')
    plt.plot(window_lengths, application_avgs_CDLL, color='red', label='CDLL')
    plt.title("Sliding Window Application")
    plt.legend(loc='best')
    plt.show()

# plot_speed()