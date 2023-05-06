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
        if str(mountain.difficulty_level) not in self.store.keys():
            self.store[str(mountain.difficulty_level)] = [mountain]
        else:
            self.store[str(mountain.difficulty_level)].append(mountain)

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

