from __future__ import annotations

from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *
from algorithms.binary_search import *

class MountainOrganiser:

    def __init__(self) -> None:
        self.rank_list = []
        self.name_list = []
        self.organiser = LinearProbeTable()

    def cur_position(self, mountain: Mountain) -> int:

        for mountains in self.rank_list:
            if mountains.name == mountain.name:
                return self.rank_list.index(mountains)
        raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:

        # self.rank_list = merge(self.rank_list, mergesort(mountains,key= lambda x:x.length), key= lambda x:x.length)
        # if len(self.rank_list) > 1:
        #     count = self.rank_list[0].length
        #     final = []
        #     temp = []
        #     last = self.rank_list[-1]
        #     for mountain in self.rank_list:
        #         if mountain.length == count and mountain != last: #length mountain sama, tp mountain bkn terakhir
        #             temp.append(mountain)
                
        #         # else: #length tdk sama dengan length sebelumnya, 
        #         temp = mergesort(temp,key=lambda x:x.name)
        #         final.extend(temp)
        #         temp = [mountain]
        #         count = mountain.length

        #         if mountain == last: #kalo mountain terahir , append ke final
        #             final.append(mountain)
               
        #     self.rank_list = final

        # self.rank_list = merge(self.rank_list, mergesort(mountains,key= lambda x:x.length), key= lambda x:x.length)
        # if len(self.rank_list) > 1:
        #     count = self.rank_list[0].length
        #     final = []
        #     temp = []
        #     boolean = False
        #     last = self.rank_list[-1]
        #     for mountain in self.rank_list:
        #         if mountain.length == count and mountain != last:
        #             temp.append(mountain)
        #         else:
        #             if mountain == last:
        #                 if mountain.length == count:
        #                     temp.append(mountain)
        #                     boolean = True
        #             temp = mergesort(temp,key=lambda x:x.name)
        #             final.extend(temp)
        #             temp = [mountain]
        #             count = mountain.length
        #             if mountain == last:
        #                 if not boolean:
        #                     final.append(mountain)
        #     self.rank_list = final

        #-----------------Yenny----------------------------------------

        # complexity = M(Log(m)) + N
        # where M is the length of input list
        # where N is the total number of mountain included so far.

        self.rank_list.extend(mountains) #O(n) where n is the length of the mountain list given
        self.rank_list = mergesort(self.rank_list,key= lambda x:x.name) #sort by name first, O(Mlog(m)) where m is the length of self.rank_list
        # self.rank_list += mergesort(mountains,key= lambda x:x.name)
        temp = []
        temp = mergesort(self.rank_list, key= lambda x:x.length) #O(Mlog(m)) where m is the length of self.rank_list
        for i in range (len(temp)): #O(N)
            self.rank_list[i] = temp[i]
        print ("self.rank_list: ",self.rank_list)


if __name__ == "__main__":
    m1 = Mountain("a", 2, 2)
    m2 = Mountain("c", 2, 1)
    m3 = Mountain("b", 3, 1)
    m4 = Mountain("m4", 3, 1)

    m5 = Mountain("f", 3, 2)
    m6 = Mountain("m6", 7, 3)
    m7 = Mountain("m7", 7, 7)

    m8 = Mountain("m8", 7, 2)
    m9 = Mountain("aa", 7, 2)
    m10 = Mountain("d", 8, 1)

    mo = MountainOrganiser()
    mo.add_mountains([m1, m2, m3,m4])
    mo.add_mountains([m5,m6,m7])
    mo.add_mountains([m8,m9,m10])

    # print([mo.cur_position(m) for m in [m1, m2]], [0, 1])
    # mo.add_mountains([m4, m3])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
    # mo.add_mountains([m5])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
    # mo.add_mountains([m7, m9, m6, m8])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])
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

    # print([mo.cur_position(m) for m in [m1, m2]], [0, 1])
    # mo.add_mountains([m4, m3])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
    # mo.add_mountains([m5])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
    # mo.add_mountains([m7, m9, m6, m8])
    # print([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])
    # self.assertRaises(KeyError, lambda: mo.cur_position(m10))


