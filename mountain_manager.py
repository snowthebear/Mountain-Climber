from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *

class MountainManager:

    def __init__(self) -> None:
        # Mountains can also be filtered by difficulty, and a list of list containing all mountains, grouped by difficulty, 
        # in ascending order, can be generated.

        self.store = LinearProbeTable() # to store the mountain

    def add_mountain(self, mountain: Mountain):
        # Add a mountain to the manager
        
        # print ("aaa", str(mountain.difficulty_level))
        # print("self.store before: ", self.store)
        # print ("self.store.keys() before: ", self.store.keys())
        if str(mountain.difficulty_level) not in self.store.keys():
            self.store[str(mountain.difficulty_level)] = [mountain]
        else:
            self.store[str(mountain.difficulty_level)].append(mountain)
        # print("self.store after: ", self.store)
        # print ("self.store.keys() after: ", self.store.keys())
        # print ()
        # print ()

    def remove_mountain(self, mountain: Mountain):
        # Remove a mountain from the manager
        if str(mountain.difficulty_level) in self.store.keys():
            if len(self.store[str(mountain.difficulty_level)]) == 1 and mountain in self.store[str(mountain.difficulty_level)]:
                del self.store[str(mountain.difficulty_level)]
            elif mountain in self.store[str(mountain.difficulty_level)] :
                self.store[str(mountain.difficulty_level)] = self.store[str(mountain.difficulty_level)].remove(mountain)


    def edit_mountain(self, old: Mountain, new: Mountain):
        # Remove the old mountain and add the new mountain.
        self.remove_mountain(old)
        self.add_mountain(new)


    def mountains_with_difficulty(self, diff: int):
        if str(diff) in self.store.keys():
            return self.store[str(diff)]
        return []

    def group_by_difficulty(self):
        sorted_list = []
        key_list = mergesort(self.store.keys(),key=lambda x:x)
        for key in key_list:
            sorted_list.append(mergesort(self.store[key],key=lambda x:x.name))
        return sorted_list
    

if __name__ == "__main__":
    m1 = Mountain("m1", 2, 2)
    m2 = Mountain("m2", 2, 9)
    m3 = Mountain("m3", 3, 6)
    m4 = Mountain("m4", 3, 1)
    m5 = Mountain("m5", 4, 6)
    m6 = Mountain("m6", 7, 3)
    m7 = Mountain("m7", 7, 7)
    m8 = Mountain("m8", 7, 8)
    m9 = Mountain("m9", 7, 6)
    m10 = Mountain("m10", 8, 4)

    mm = MountainManager()
    mm.add_mountain(m1)
    mm.add_mountain(m2)
    mm.add_mountain(m3)
    mm.add_mountain(m6)
    mm.add_mountain(m7)

    def make_set(my_list):
        """
        Since mountains are unhashable, add a method to get a set of all mountain ids.
        Ensures that we can compare two lists without caring about order.
        """
        return set(id(x) for x in my_list)
    

    print(make_set(mm.mountains_with_difficulty(3)), make_set([m3]))
    print(make_set(mm.mountains_with_difficulty(4)), make_set([]))
    print(make_set(mm.mountains_with_difficulty(7)), make_set([m6, m7]))


