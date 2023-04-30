from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *

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
        # self.store[mountain.name,mountain]
        self.list_mountain.append(mountain)
        

    def remove_mountain(self, mountain: Mountain):
        # Remove a mountain from the manager
        if mountain in self.list_mountain:
            self.list_mountain.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        # Remove the old mountain and add the new mountain.
        self.list_mountain.remove(old)
        self.list_mountain.add(new)


    def mountains_with_difficulty(self, diff: int):
        #  Return a list of all mountains with this difficulty.
        difficulty_list = []
        for mountain in self.list_mountain:
            if mountain.difficulty_level == diff:
                difficulty_list.append(mountain)
        return difficulty_list

    def group_by_difficulty(self):
        # return a sorted list of the mountains by its difficulty.
        self.list_mountain = mergesort(self.list_mountain, key=lambda x: x.difficulty_level) # only sorting by the difficulty of mountain , but for the same difficulty level, name may be still not in alphabatical order
        print(self.list_mountain)
        temp = self.list_mountain[0].difficulty_level # just a temp variable which get the value from the least difficulty level
        temp_list = [] # this list to store only same difficulty level mountains. once difficulty level goes to the next integer , this list will be clear for the next same difficulty level
        final = [] # this list to store the final result
        for mountain in self.list_mountain:
            if self.list_mountain.index(mountain) == len(self.list_mountain) - 1: # if this loop is the last element in the list , means there is nothing next to loop , sort the temp list and add to final , done for the sorting step
                if mountain.difficulty_level == temp: # if is last element and same difficulty level as the previous element , add to temo and sort together
                    temp_list.append(mountain)
                    temp_list = mergesort(temp_list, key=lambda x: x.name)
                    final.append(temp_list) # temp list is a list , append to another list will get a list in a list
                else: # if difficulty level is different , means that the last element have its own group which is one and only of this difficulty level
                    temp_list = mergesort(temp_list, key=lambda x: x.name) # sort the temp list and append to final first , this is the previous difficulty level
                    final.append(temp_list)
                    final.append([mountain]) # then add this last element which is the only one for this difficulty level , only one so no need to sort , straight add into the final . and to make it a list , make append([mountain])
            elif temp == mountain.difficulty_level: # if is not the last element and same difficulty level as the previous difficulty level
                temp_list.append(mountain) # means there r in the same group , but we r not sure whether there is still the same difficulty level for the next mountain , so dont sort first , just append to be in same group
            elif temp != mountain.difficulty_level: # when the difficulty level is different , sort and clear the temp list
                temp_list = mergesort(temp_list, key=lambda x: x.name) # sort and add to final list
                final.append(temp_list)
                temp = mountain.difficulty_level # now set the temp dificulty level to the current different one for the next group
                temp_list = [mountain] # this mountain be the first in the temp list of this group of difficulty level
        return final # will be a list of several lists

