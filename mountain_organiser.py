from __future__ import annotations

from mountain import Mountain
from algorithms.mergesort import *

class MountainOrganiser:

    def __init__(self) -> None:
        self.rank_list = []

    def cur_position(self, mountain: Mountain) -> int:

        for mountains in self.rank_list:
            if mountains.name == mountain.name:
                return self.rank_list.index(mountains)
        raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:

        self.rank_list.extend(mountains)
        self.rank_list = mergesort(self.rank_list , key = lambda x:x.length)
        temp = self.rank_list[0].length
        temp_list = []
        final = []
        for mountain in self.rank_list:
            if self.rank_list.index(mountain) == len(self.rank_list) - 1:
                if mountain.length == temp:
                    temp_list.append(mountain)
                    temp_list = mergesort(temp_list, key=lambda x: x.name)
                    final.extend(temp_list)
                else:
                    temp_list = mergesort(temp_list, key=lambda x: x.name)
                    final.extend(temp_list)
                    final.append(mountain)
            elif temp == mountain.length:
                temp_list.append(mountain)
            elif temp != mountain.length:
                temp_list = mergesort(temp_list, key=lambda x: x.name)
                final.extend(temp_list)
                temp = mountain.length
                temp_list = [mountain]
        self.rank_list = final





