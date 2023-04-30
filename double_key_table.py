from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        self.count = 0
        self.sizes = self.TABLE_SIZES
        self.internal_sizes = self.TABLE_SIZES
        self.size_index = 0

        if sizes is not None:
            self.sizes = sizes
        
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes

        self.outer_hash =  ArrayR(self.sizes[self.size_index]) #because depends on the TABLE_SIZE


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """

        top_pos = self.hash1(key1)
        # print(type(self.table_size))
        for a in range (self.table_size):
            if self.outer_hash[top_pos] is None:
                if is_insert:
                    inner = LinearProbeTable(self.internal_sizes) # untuk value outer table
                    inner.hash = lambda k: self.hash2(k, inner)
                    self.outer_hash[top_pos] = (key1, inner) #setting ke outer
                    self.count +=1
                    bottom_pos = self.outer_hash[top_pos][1]._linear_probe(key2, is_insert) #access inner table, call the linear probe
                    return (top_pos, bottom_pos)
                else:
                    raise KeyError(top_pos)
            elif self.outer_hash[top_pos][0] == key1:
                #cek inner ha
                # print("x")
                bottom_pos = self.outer_hash[top_pos][1]._linear_probe(key2, is_insert)
                return (top_pos, bottom_pos)
            else:
                top_pos = (top_pos + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError


    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        raise NotImplementedError()

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        raise NotImplementedError()

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        (top_pos, bottom_pos) = self._linear_probe(key[0], key[1], False)
        return self.outer_hash[top_pos][1][key[1]]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        # if len(self) == len(self.sizes) and key[0] not in self:
        #     raise ValueError("Cannot insert into a full table.")
        
        (top_pos, bottom_pos) = self._linear_probe(key[0], key[1], True)
        self.outer_hash[top_pos][1][key[1]] = data
        print(key, (top_pos,bottom_pos), data)
        # if self.outer_hash[position] is None:
            # self.count += 1
        # self.outer_hash[position] = (key, data)
        ## self...[key[1]] = data
        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos = self._linear_probe(key,False)
        self.sizes[pos] = None
        self.count -= 1
        pos = (pos + 1) % len(self.sizes)

        # if key not in self.table_size:
        #     raise KeyError("key doesnt exist")

        while self.sizes[pos] is not None:
            item = self.sizes[pos]
            self.sizes[pos] = None
            self.count -= 1
            self[item[0]] = item[1] #using set magic method
            pos = (pos + 1) % len(self.sizes)

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.sizes[self.size_index]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        new_string = ""
        for item in self.sizes:
            if item is not None:
                (key, value) = item
                new_string += "(" + str(key) + "," + str(value) + ")\n"
        return new_string

if __name__ == "__main__":
    dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
    dt.hash1 = lambda k: ord(k[0]) % 12
    dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

    dt["Tim", "Jen"] = 1
    dt["Amy", "Ben"] = 2
    dt["May", "Ben"] = 3
    dt["Ivy", "Jen"] = 4
    dt["May", "Tom"] = 5
    dt["Tim", "Bob"] = 6
    print(dt["Tim","Jen"])
    print(dt["Tim","Bob"])