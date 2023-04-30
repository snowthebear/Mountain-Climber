from mountain import Mountain
from data_structures.hash_table import LinearProbeTable

class MountainManager:

    def __init__(self) -> None:
        # Mountains can also be filtered by difficulty, and a list of list containing all mountains, grouped by difficulty, 
        # in ascending order, can be generated.
        
        # The ADT required would be hashtable 
        # (hence choose between LinearProbeTable, DoubleKeyedTable or Infinite Depth Hash Table).

        self.store = LinearProbeTable() # to store the mountain
        self.list_mountain = []


    def add_mountain(self, mountain: Mountain):
        # Add a mountain to the manager
        self.store[mountain]
        

    def remove_mountain(self, mountain: Mountain):
        # Remove a mountain from the manager
        del self.store[mountain[0]]

    def edit_mountain(self, old: Mountain, new: Mountain):
        # Remove the old mountain and add the new mountain.
        pass

    def mountains_with_difficulty(self, diff: int):
        #  Return a list of all mountains with this difficulty.
        pass

    def group_by_difficulty(self):
        # return a sorted list of the mountains by its difficulty.
        pass
