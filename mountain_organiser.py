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
