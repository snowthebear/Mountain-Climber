from __future__ import annotations
from typing import Generic, TypeVar
from data_structures.linked_stack import *

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self,sizes = None) -> None:
        """
        Big-O notation: O(self.TABLE_SIZE) because it depends on the size of the given TABLE_SIZE
        """

        if sizes is not None:
            self.TABLE_SIZE = sizes
        self.level = 0
        self.table = ArrayR(self.TABLE_SIZE)
        self.count = 0

    def hash(self, key: K) -> int:
        """
        Big-O notation: O(1) because it is returning a constant value.
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Big-O notation: O(self.get_location() + n)
        """
        
        locations = self.get_location(key)
        for x in locations:
            return self.table[x][1]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Big-O notation: Best: O(hash(key)) --> O(1), where the position of the table is None.
                        Worst: O(hash(key) + n*(hash(key))) --> O(n), 
                               where n is the comparison of copy < len(key) and copy < len(original_key) and key[copy] == original_key[copy].
        """
        position = self.hash(key)
        if self.table[position] is None:
            self.table[position] = (key,value)
            self.count += 1
        elif isinstance(self.table[position][1],InfiniteHashTable):
            self.table[position][1][key] = value
            self.count += 1 # why ?????
        elif self.table[position][0] == key:
            self.table[position] = (key,value)
        else:
            next_level = InfiniteHashTable()
            copy = self.level + 1
            original_key = self.table[position][0]
            original_value = self.table[position][1]
            self.table[position] = (key[:self.level + 1], next_level)
            while copy < len(key) and copy < len(original_key) and key[copy] == original_key[copy]:
                selve = next_level
                next_level.level = copy
                position_ = next_level.hash(key)
                next_level = InfiniteHashTable()
                selve.table[position_] = (key[:copy + 1], next_level)
                copy += 1
            next_level.level = copy
            position1 = next_level.hash(original_key)
            next_level.table[position1] = (original_key, original_value)
            position2 = next_level.hash(key)
            next_level.table[position2] = (key, value)
            self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Big-O notation: Best: O(hash(key)), when the value of given position is the key.
                        Worst: O(hash(key) + ) ???
        """
        position = self.hash(key)
        copy = ()
        count = 0
        if isinstance(self.table[position][1], InfiniteHashTable):
            if isinstance(self.table[position][1].table[self.table[position][1].hash(key)][1], InfiniteHashTable):
                del self.table[position][1][key]
                self.count -= 1

            elif self.table[position][1].table[self.table[position][1].hash(key)][0] == key:
                self.table[position][1].table[self.table[position][1].hash(key)] = None
                self.count -= 1

            for i in self.table[position][1].table:
                if i is not None:
                    count += 1
                    copy = i

            if count <= 1:
                if not isinstance(copy[1],InfiniteHashTable):
                    self.table[position] = copy

        elif self.table[position][0] == key:
            self.table[position] = None
            self.count -= 1

        else:
            raise KeyError

    def __len__(self):
        """
        Big-O notation: O(1) because it is only returning a constant value (self.count)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.

        Big-O notation: O(self.table) where self.table is the array with the size of self.TABLE_SIZE
        """
        result = str(self.table)
        return result

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Big-O notation: Best: O(hash(key)) when the key is equals to the self.table[position][0]: 
                        Worst: O(hash(key) + n) when it needs to extend the list.

        """
        position = self.hash(str(key))
        location = []
        if self.table[position] is None :
            raise KeyError
        elif isinstance(self.table[position][1], InfiniteHashTable):
            location.append(position)
            location.extend(self.table[position][1].get_location(key))
        elif key == self.table[position][0]:
            location.append(position)
        elif key != self.table[position][0]:
            raise KeyError
        return location

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
