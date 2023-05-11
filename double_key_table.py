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

        Big-O notation: Best - O(hash1(key1) + hash1(key2)) --> O(len(key1) + len(key2)), when the first position is empty
                        Worst - O(hash1(key1) + n * (hash2(key2) + _linear_probe())) --> O(len(key1) + n * (len(key2) + N*comp(K)))
                                where n is the length of the table_size, hash1 is len(key), hash2 is len(key), 
                                and _linear_probe is O(hash(key) + N*comp(K)) where N is the table size.
        """

        top_pos = self.hash1(key1) #O(hash1(key))

        for a in range (self.table_size): #O(n) 
            if self.outer_hash[top_pos] is None:
                if is_insert:
                    inner = LinearProbeTable(self.internal_sizes) # untuk value outer table
                    inner.hash = lambda k: self.hash2(k, inner) #O(len(key))
                    self.outer_hash[top_pos] = (key1, inner) #setting ke outer
                    self.count +=1
                    bottom_pos = self.outer_hash[top_pos][1]._linear_probe(key2, is_insert) #access inner table, call the linear probe, 
                    return (top_pos, bottom_pos)
                else:
                    raise KeyError(top_pos)
                
            elif self.outer_hash[top_pos][0] == key1:
                #cek inner hash
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
                    yield self.outer_hash[x][0] #O(n) or O(1) ?
        
        else:
            pos = self.hash1(key) #O(hash)
            for i in range (self.outer_hash[pos][1].table_size): #O(n)
                if self.outer_hash[pos][1] is not None:
                    for i in self.outer_hash[pos][1].keys(): #(On)
                        yield i
                
        # # res.append(None)
        # # print ("res: ", res)
        # # print (len(res))
        # list_res = iter(res)
        # i = 0
        # # while i != len(res):
        # #     print ("i: ", i)
        # #     # if i == len(res)-2:
        # #     #     return (list_res)
        # #     # print ("res: ",res)
        # #     yield res[i]
        # #     i+=1
        # raise StopIteration

        # for i in range (len(res)):
        #     print ("res i: ", res[i])
        #     if ([res[i]]) is not None:
        #         print ("AAA")
        #         yield res[i]
            # return(iter(res))
            
                # print ("res[i]: ", res[i])
                

        # for item in list_res:
        #     if next(list_res) is None:
        #         print ("AAA")
        #         return (list_res)
        #     yield item
        # return (iter(res))
    
    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Big-O notation: Best: O(n) where n is the length of the table size, best case when the key is None
                        Worst: O(hash1(key) + n) --> O(len(key) + n) where n is the length of the table size, worst case when the key is not None.
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
                        Worst - O(hash1(key) + n * (comp(k1) + m)) --> O(len(key) + n * (comp(k1) + m)) worst case is when the key is given.
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

        Big-O notation: O(_linear_probe) --> O(hash1(key) + n * (len(key) + N*comp(K)))
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
                               = O(len(key1) + n * (len(key2) + N*comp(K)) + N*hash(key)+ N^2*comp(K))

        """

        top_pos, bottom_pos = self._linear_probe(key[0], key[1], False)

        del self.outer_hash[top_pos][1][key[1]] #using Linear Probe table delete
        if len(self.outer_hash[top_pos][1]) == 0:
            self.count -=1
            self.outer_hash[top_pos] = None
        top_pos = (top_pos + 1) % self.table_size
        # print ("key[0], key[1]: ", key[0], key[1])

        #-------------------------------------------------------------
        # if self.outer_hash[top_pos] is None:
        #     while self.outer_hash[top_pos] is not None:
        #         # key1, value = self.outer_hash[top_pos]
        #         item = self.outer_hash[top_pos]
        #         # print ("key1 before: ",item[0])
        #         self.outer_hash[top_pos][1][key[1]] = None
        #         # print ("a: ",self.outer_hash[top_pos][1][item[1]])
        #         # print ("key1 after: ",item[1])
        #         item = self.outer_hash[top_pos]
        #         # newpos = value._linear_probe(key1, True)
        #         # print ("newpos: ",newpos)
        #         # print ((key1, value))
        #         # self.outer_hash[newpos] = (key1, value)
        #         # list_key = value.keys()
        #         # # self.outer_hash[top_pos][1][key[1]] = None

        #         # # self.outer_hash[top_pos] = None
        #         # for key2 in list_key:
        #         #     self[key1, key2] = newpos #using set magic method
        #         # # self.count -= 1
        #         # # # print(self[item[0]])
        #         top_pos = (top_pos + 1) % self.table_size
            #----------------------------------------------
                # key2, value = self.outer_hash[top_pos]
                # self.outer_hash[top_pos] = None
                # # Reinsert.
                # newpos = self._linear_probe(key[0],key2, True)
                # self.outer_hash[newpos] = (key2, value)
                # top_pos = (top_pos + 1) % self.table_size
        # else:
        #     self.outer_hash[top_pos][1][key[0]] = None
        #     # top_pos = (top_pos + 1) % self.table_size
        # # top_pos = (top_pos + 1) % self.table_size

        
        # print ("top_pos after: ",top_pos)
        # print ("pos: ",pos)

        

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
                    

        #-----------------------------------------------

        # print(self.sizes[self.size_index])
        # print (self.table_size)
        # print (f"self.outer_hash[0][1]: {self.outer_hash[0][1]} ", end ="")


        # for i in range (len(self.outer_hash)): #inner table
        #     # print ("len(self.outer_hash)): ",i)
        #     print (type(self.outer_hash[i])) #tuple
        #     if self.outer_hash[i] is not None:
        #         print (len(self.outer_hash[i]))
        #         print (type(self.outer_hash[i][1])) #data structure
        #         print("outerhash[i]: ", self.outer_hash[i][1])
        #         print ("self.internal_sizes[self.size_index]: ", self.internal_sizes[self.size_index])
        #         print ("len(self.internal_sizes)",len(self.internal_sizes))
        #         if len(self.outer_hash[i][1]) >= len(self.internal_sizes) // 2:
        #             self.outer_hash[i][1]._rehash()
        #             print ("3r")

        # print ("table_size: ", self.table_size)
        # print ("self.outer_hash: ", len(self.outer_hash))
        # print("self.sizes[self.size_index]: ",self.sizes[self.size_index])
        # print ("self.sizes[self.size_index] // 2: ", self.sizes[self.size_index] // 2)
        # print ("count:",self.count)

        # for i in range (len(self.outer_hash)): #inner table
        #     if len(self.outer_hash[i][1]) == self.internal_sizes[self.size_index]:
        #         old_array = self.outer_hash
        #         self.size_index += 1
        #         if self.size_index == len(self.outer_hash):
        #             # print (self.size_index, len(self.outer_hash))
        #             # Cannot be resized further.
        #             return
        #         self.outer_hash = ArrayR(self.sizes[self.size_index])
        #         # print (len(self.outer_hash))
        #         self.count = 0
        #         for item in old_array:
        #             if item is not None:
        #                 key, value = item
        #                 self[key] = value
        
    
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

        Big-O notaion: O(n) where n is the length of the sizes.
        """
        new_string = ""
        for item in self.sizes:
            if item is not None:
                (key, value) = item
                new_string += "(" + str(key) + "," + str(value) + ")\n"
        return new_string

if __name__ == "__main__":
    # dt = DoubleKeyTable(sizes=[3, 5], internal_sizes=[3, 5])
    # dt.hash1 = lambda k: ord(k[0]) % dt.table_size
    # dt.hash2 = lambda k, sub_table: ord(k[-1]) % sub_table.table_size
    # dt["Pip", "Bob"] = 4
    # (dt.table_size, 5)

    # print (dt._rehash())

    # dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
    # dt.hash1 = lambda k: ord(k[0]) % 12
    # dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

    # dt["Tim", "Jen"] = 1
    # dt["Amy", "Ben"] = 2
    # dt["Tim", "Kat"] = 3

    # print(dt._linear_probe("Tim", "Kat", False), (0, 1))

    # del dt["Tim", "Jen"]
    # # We can't do this as it would create the table.
    # # self.assertEqual(dt._linear_probe("Het", "Bob", True), (1, 3))
    # del dt["Tim", "Kat"]
    # # Deleting again should make space for Het.
    # dt["Het", "Bob"] = 4
    # print(dt._linear_probe("Het", "Bob", False), (0, 3))

    # # print(KeyError, lambda: dt._linear_probe("Tim", "Jen", False))
    # dt["Tim", "Kat"] = 5
    # print(dt._linear_probe("Tim", "Kat", False), (1, 1))

    # dt = DoubleKeyTable()
    

    # key_iterator = dt.iter_keys("May")
    # value_iterator = dt.iter_values()

    # key = next(key_iterator)
    # print("key: ",key, ["May", "Kim"])
    # key = next(key_iterator)
    # print("key: ",key, ["May", "Kim"])
    

    # value = next(value_iterator)
    # # print("value. : ",value, [1, 2])
    # value = next(value_iterator)
    # # print(value, [1, 2])

    # del dt["May", "Jim"]
    # del dt["Kim", "Tim"]
    # print(next(key_iterator))
    # print(next(key_iterator))

    dt = DoubleKeyTable()
    # dt["May", "Jim"] = 1
    # dt["Kim", "Tim"] = 2
    dt["May", "Jim"] = 1
    dt["May", "a"] = 4
    dt["Kim", "Tim"] = 2
    dt["Kim", "Jim"] = 3

    key_iterator = dt.iter_keys()
    value_iterator = dt.iter_values()

    key = next(key_iterator)
    print(key, ["May", "Kim"])
    # print ("aa",dt.iter_keys())
    key = next(key_iterator)
    print (key)
    print(key, ["May", "Kim"])
    # # key = next(key_iterator)
    # print(key, ["May", "Kim"])
    # key = next(key_iterator)
    # print(key, ["May", "Kim"])
    # # print(key, ["May", "Kim"])
    # value = next(value_iterator)
    # print(value, [1, 2])
    # value = next(value_iterator)
    # print(value, [1, 2])
    # value = next(value_iterator)
    # print(value, [1, 2])
    # value = next(value_iterator)
    # print(value, [1, 2])
    # value = next(value_iterator)

    # del dt["May", "Jim"]
    # del dt["Kim", "Tim"]

    # Retrieving the next value should either raise StopIteration or crash entirely.
    # Note: Deleting from an element being iterated over is bad practice
    # We just want to make sure you aren't returning a list and are doing this
    # with an iterator.
    # self.assertRaises(BaseException, lambda: next(key_iterator))
    # self.assertRaises(BaseException, lambda: next(value_iterator))

    


    
