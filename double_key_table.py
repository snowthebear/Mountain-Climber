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

    Big-O notation: O(1) because it is only assignment to the class variable.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Big-O notation: O(self.size_index) because it depends on self.size_index

        """
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

        Big-O notation: Best - O(hash1(key1) + hash1(key2)) --> O(len(key1) + comp(key1) + len(key2) + comp(key2)), when the key is matched at the first iteration (searching), and the first position is empty
                        Worst - O(hash1(key1) + n * (hash2(key2) + _linear_probe())) --> O(len(key1) + n * (len(key2) + N*comp(K)))
                                where n is the length of the table_size, hash1 is len(key), hash2 is len(key), 
                                and _linear_probe is the inner table O(hash(key) + N*comp(K)) where N is the table size and K is the key of inner table.
        """

        top_pos = self.hash1(key1) #O(hash1(key))
        #O(len(key1) + n*(len(key2) + N*comp(K))))
        for a in range (self.table_size): #O(n) 
            if self.outer_hash[top_pos] is None:
                if is_insert:
                    inner = LinearProbeTable(self.internal_sizes) # for value outer table
                    inner.hash = lambda k: self.hash2(k, inner) #O(len(key))
                    self.outer_hash[top_pos] = (key1, inner) #setting ke outer
                    self.count +=1
                    bottom_pos = self.outer_hash[top_pos][1]._linear_probe(key2, is_insert) #access inner table, call the linear probe, 
                    return (top_pos, bottom_pos)
                else:
                    raise KeyError(top_pos)
                
            elif self.outer_hash[top_pos][0] == key1:
                #check inner hash
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

        Big-O notation: Best - O(n) where n is the length of the table size and when the key is None.
                        Worst - O(hash1(key) + n^2) --> O(len(key) + n^2) where n is the length of inner table size from the position of element given by hash1(key).
        """

        if key is None:
            for x in range(self.table_size): #O(n)
                if self.outer_hash[x] is not None:
                    yield self.outer_hash[x][0] #O(1)
        
        else:
            pos = self.hash1(key) #O(hash)
            for i in range (self.outer_hash[pos][1].table_size): #O(n)
                if self.outer_hash[pos][1] is not None:
                    for i in self.outer_hash[pos][1].keys(): #O(n)
                        yield i
    
    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Big-O notation: Best: O(n) where n is the length of the table size, best case when the key is None
                        Worst: O(hash1(key) + n) --> O(len(key) + n * comp(key)) where n is the length of the table size, worst case when the key is not None.
        """
    
        if key is None:
            res = []
            for x in range(self.table_size):
                if self.outer_hash[x] is not None:
                    res.append(self.outer_hash[x][0])
            return res

        else:
            top_pos = self.hash1(key) #O(len(key))
            for i in range (self.table_size):
                if self.outer_hash[top_pos][0] == key:
                    return self.outer_hash[top_pos][1].keys()
                else:
                    top_pos = (top_pos + 1) % self.table_size
        

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Big-O notation: Best - O(n) where n is the length of the table size and when the key is None.
                        Worst - O(hash1(key) + n^2) --> O(len(key) + n^2), where n is the length of inner table size from the position of element given by hash1(key).
                                the first n is from the for loop, and the second n is for se
        """

        if key is None: #if key is default (None)
            for x in range(self.table_size): #loop through the table # O(n)
                if self.outer_hash[x] is not None: # if there is something in the table, return the values in that position.
                    yield self.outer_hash[x][1].values()[0] #O(n) or O(1)?

        else: #if key is not None
            pos = self.hash1(key) #O(hash1() --> len(key))
            for i in range (self.outer_hash[pos][1].table_size): #O(n)
                if self.outer_hash[pos] is not None:
                    for i in self.outer_hash[pos][1].values(): #O(n)
                        yield i
                

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Big-O notation: Best - O(n) where n is the length of the table size, and best case is when the key is None.
                        Worst - O(hash1(key) + n * (comp(k1) + m)) --> O(len(key) + n * (comp(k1) + m)) worst case is when the key is given and it the 2nd key is matches.
                                where n is the the length of the table size, and comp(k1) is the comparison of whether the element is the key,
                                and m where it returns the values with .values()
        """
        if key is None: #if key is default (None)
            res = []
            for x in range(self.table_size): #loop through the table
                if self.outer_hash[x] is not None: # if there is something in the table, return the values in that position.
                    res += self.outer_hash[x][1].values()
            return res
        
        else:
            top_pos = self.hash1(key)
            for i in range (self.table_size):
                if self.outer_hash[top_pos][0] == key:
                    return self.outer_hash[top_pos][1].values()
                else:
                    top_pos = (top_pos + 1) % self.table_size

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

        Big-O notation: Best - O(hash1(key1) + hash1(key2)) --> O(len(key1) + comp(key1) + len(key2) + comp(key2)), when the key is matched at the first iteration (searching), and the first position is empty
                        Worst - O(hash1(key1) + n * (hash2(key2) + _linear_probe())) --> O(len(key1) + n * (len(key2) + N*comp(K)))
                                where n is the length of the table_size, hash1 is len(key), hash2 is len(key), 
                                and _linear_probe is the inner table O(hash(key) + N*comp(K)) where N is the table size and K is the key of inner table.
        """
        (top_pos, bottom_pos) = self._linear_probe(key[0], key[1], False)
        return self.outer_hash[top_pos][1][key[1]]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Big-O notation: Best: O(hash1(key) + n * (len(key) + N*comp(K))), when the table is not filled more than half, which also means do not need to rehash.
                        Worst: O(hash1(key) + n * (len(key) + N*comp(K)) + _rehash()) --> 
                               O(len(key1) + n * (len(key2) + N*comp(K)) + _rehash()), when the table is require to rehash.
        """
        
        (top_pos, bottom_pos) = self._linear_probe(key[0], key[1], True)
        self.outer_hash[top_pos][1][key[1]] = data
        if len(self) > self.table_size / 2:
            self._rehash()
        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Big-O notation: Best: O(hash1(key1) + hash1(key2) + hash(key)) --> O(len(key1) + len(key2))
                        Worst: O(_linear_probe + N*hash(key)+N^2*comp(K)) when deleting item is midway through large chain.
                               O(hash1(key) + n * (len(key2) + N*comp(K)) + N*hash(key)+ N^2*comp(K))
                               = O(len(key1) + n * (len(key2) + N*comp(K)) + M*hash(key)+ M^2*comp(K))
                                where n is the length of the table_size, hash1 is len(key), hash2 is len(key), 
                                and _linear_probe is the inner table O(hash(key) + N*comp(K)) where N is the table size and K is the key of inner table.
                                and it is worst when deleting item is midway through large chain.

        """

        top_pos, bottom_pos = self._linear_probe(key[0], key[1], False)

        del self.outer_hash[top_pos][1][key[1]] #using Linear Probe table delete
        if len(self.outer_hash[top_pos][1]) == 0:
            self.count -=1
            self.outer_hash[top_pos] = None
        top_pos = (top_pos + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """

        old_array = self.outer_hash
        self.size_index += 1
        if self.size_index == len(self.sizes):
            # Cannot be resized further.
            return

        self.outer_hash :ArrayR[tuple[K1, LinearProbeTable]] = ArrayR(self.sizes[self.size_index])

        for item in old_array:
            if item is not None:
                key, inner_table = item
                list_key = inner_table.keys() #linear probe, key inner table
                for key2 in list_key: #finding the inner key
                    (top_pos, bottom_pos) = self._linear_probe(key, key2, True)
                    self.outer_hash[top_pos] = (key, inner_table)
                    
    
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        Big-O notation = O(1) because it is only returning a constant.
        """
        return self.sizes[self.size_index]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Big-O notation: O(1) because it is only returning a constant (self.count)
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
    


    