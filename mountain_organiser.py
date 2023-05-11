# from __future__ import annotations

from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *
from algorithms.binary_search import *

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Big-O notation: O(1) because only declaration of an empty list.
        """
        self.rank_list = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Big-O notation: O(log(N)) where N is the total number of mountain included so far.
        """
        # Finds the rank of the provided mountain given all mountains included so far. See below for an example. 
        # Raises KeyError if this mountain hasn't been added yet.

        if mountain in self.rank_list:
            x = binary_search(self.rank_list, mountain)
            return x
        
        raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Big-O notation: O(M log(M) + N) where M is the length of input list, and N is the total number of mountains included so far.
        """
        mount_list = mergesort(mountains, lambda x:x.name) #nlogn
        self.rank_list = merge(self.rank_list,mount_list,key = lambda x:x.name) #O(2nlogn + O(n))
        temp = []
        temp = mergesort(self.rank_list, key= lambda x:x.length) #O(Mlog(m)) where m is the length of self.rank_list
        self.rank_list = temp

if __name__ == "__main__":
    # m1 = Mountain("a", 2, 2)
    # m2 = Mountain("c", 2, 1)
    # m3 = Mountain("b", 3, 1)
    # m4 = Mountain("m4", 3, 1)

    # m5 = Mountain("f", 3, 2)
    # m6 = Mountain("m6", 7, 3)
    # m7 = Mountain("m7", 7, 7)

    # m8 = Mountain("m8", 7, 2)
    # m9 = Mountain("aa", 7, 2)
    # m10 = Mountain("d", 8, 1)

    # mo = MountainOrganiser()
    # mo.add_mountains([m1, m2, m3,m4])
    # mo.add_mountains([m5,m6,m7])
    # mo.add_mountains([m8,m9,m10])

    # print([mo.cur_position(m) for m in [m1, m2]], [0, 1])
    # mo.add_mountains([m4, m3])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
    # mo.add_mountains([m5])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
    # mo.add_mountains([m7, m9, m6, m8])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])
    # self.assertRaises(KeyError, lambda: mo.cur_position(m10))


    m1 = Mountain("m1", 2, 2)
    m2 = Mountain("m2", 2, 9)
    m3 = Mountain("m9", 3, 6)
    m4 = Mountain("m4", 3, 1)
    m5 = Mountain("m5", 4, 6)
    m6 = Mountain("m6", 7, 3)
    m7 = Mountain("m7", 7, 7)
    m8 = Mountain("m8", 7, 8)
    m9 = Mountain("m3", 7, 6)
    m10 = Mountain("m10", 8, 4)


    mo = MountainOrganiser()
    mo.add_mountains([m1, m2])

    print("aa: ",[mo.cur_position(m) for m in [m1, m2]], [0, 1])
    mo.add_mountains([m4, m3])
    print([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
    mo.add_mountains([m5])
    print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
    mo.add_mountains([m7, m9, m6, m8])
    print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])
    # self.assertRaises(KeyError, lambda: mo.cur_position(m10))


    # m1 = Mountain("m1", 2, 2)
    # m2 = Mountain("m2", 2, 9)
    # m3 = Mountain("m3", 3, 6)
    # m4 = Mountain("m4", 3, 1)
    # m5 = Mountain("m5", 4, 6)
    # m6 = Mountain("m6", 7, 3)
    # m7 = Mountain("m7", 7, 7)
    # m8 = Mountain("m8", 7, 8)
    # m9 = Mountain("m9", 7, 6)
    # m10 = Mountain("m10", 8, 4)

    # mo = MountainOrganiser()
    # mo.add_mountains([m1, m2])

    # # print([mo.cur_position(m) for m in [m1, m2]], [0, 1])
    # mo.add_mountains([m4, m3])
    # # print([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
    # mo.add_mountains([m5])
    # # # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
    # mo.add_mountains([m7, m9, m6, m8])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])

    # mo.add_mountains([m3])
    # print ([mo.cur_position(m) for m in [m3]], [0, 1])

