from __future__ import annotations

from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *
from algorithms.binary_search import *

class MountainOrganiser:

    def __init__(self) -> None:
        self.rank_list = []
        self.organiser = LinearProbeTable()

    def cur_position(self, mountain: Mountain) -> int:

        for mountains in self.rank_list:
            if mountains.name == mountain.name:
                return self.rank_list.index(mountains)
        raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:

        self.rank_list = merge(self.rank_list, mergesort(mountains,key= lambda x:x.length), key= lambda x:x.length)
        if len(self.rank_list) > 1:
            count = self.rank_list[0].length
            final = []
            temp = []
            boolean = False
            last = self.rank_list[-1]
            for mountain in self.rank_list:
                if mountain.length == count:
                    temp.append(mountain)
                else:
                    if mountain == last:
                        if mountain.length == count:
                            temp.append(mountain)
                            boolean = True
                    temp = mergesort(temp,key=lambda x:x.name)
                    final.extend(temp)
                    temp = [mountain]
                    count = mountain.length
                    if mountain == last:
                        if not boolean:
                            final.append(mountain)
            self.rank_list = final
