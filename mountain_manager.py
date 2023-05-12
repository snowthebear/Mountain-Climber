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
    