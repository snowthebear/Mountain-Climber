from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *
from double_key_table import DoubleKeyTable

class MountainManager:

    def __init__(self) -> None:
        """
        Big-O notation: O(1) because we only assign to the variable.
        """
        # Mountains can also be filtered by difficulty, and a list of list containing all mountains, grouped by difficulty, 
        # in ascending order, can be generated.

        self.store = DoubleKeyTable() #to store the mountain
        self.mountain_list =[]

    def add_mountain(self, mountain: Mountain):
        """
        Big-O notation: O(1) because we assume that all DubleKeyTable() function is O(1)
        """
        try:
            self.store[str(mountain.difficulty_level), mountain.name] = mountain

        except:
            raise ValueError("Value not found")

    def remove_mountain(self, mountain: Mountain):
        """
        Big-O notation: O(n) where n is the iteration in self.store.keys().

        """

        if str(mountain.difficulty_level) in self.store.keys():
            del self.store[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Remove the old mountain and add the new mountain.

        Big-O notation: O(1) since we assume that every function in DoubleKeyTable() is O(1)
        """
        self.remove_mountain(old)
        self.add_mountain(new)


    def mountains_with_difficulty(self, diff: int):
        """
        Big-O notation: 
        """
        try:
            return (self.store.values(str(diff)))
        except:
            return []

    def group_by_difficulty(self):
        """
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        
        Big-O notation: O(n) where n is the number of elements in the key of the table.

        """
        # self.store.values is sorted by the name
        sorted_list = []
        for i in self.store.keys():
            sorted_list += [self.store.values(i)]
        
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
    

    # print(make_set(mm.mountains_with_difficulty(3)), make_set([m3]))
    # print(make_set(mm.mountains_with_difficulty(4)), make_set([]))
    # print(make_set(mm.mountains_with_difficulty(7)), make_set([m6, m7]))

    mm.add_mountain(m4)
    mm.add_mountain(m5)
    mm.add_mountain(m8)
    mm.add_mountain(m9)

    res = mm.group_by_difficulty()
    # print(len(res), 4)
    print(make_set(res[0]), make_set([m1, m2]))
    print(make_set(res[1]), make_set([m3, m4]))
    print(make_set(res[2]), make_set([m5]))
    print(make_set(res[3]), make_set([m6, m7, m8, m9]))

    mm.add_mountain(m10)
    # mm.remove_mountain(m5)

    res = mm.group_by_difficulty()
    # print(len(res), 4)

    # print(make_set(res[3]), make_set([m10]))



