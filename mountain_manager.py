from mountain import Mountain
from data_structures.hash_table import LinearProbeTable
from algorithms.mergesort import *
from double_key_table import DoubleKeyTable

class MountainManager:

    def __init__(self) -> None:
        # Mountains can also be filtered by difficulty, and a list of list containing all mountains, grouped by difficulty, 
        # in ascending order, can be generated.

        # self.store = LinearProbeTable() # to store the mountain
        self.store = DoubleKeyTable()
        self.mountain_list =[]

    def add_mountain(self, mountain: Mountain):
        # Add a mountain to the manager
        # print ("aaa", str(mountain.difficulty_level))
        # print("self.store before: ", self.store)
        # print ("self.store.keys() before: ", self.store.keys())
        #------------------------------------------------------------
        try:
        # if str(mountain.difficulty_level) not in self.store.keys():
            self.store[str(mountain.difficulty_level), mountain.name] = mountain

        except:
            raise ValueError("ERROR WOI BEGO")
        # else:
        #     self.store[str(mountain.difficulty_level), mountain.name].append(mountain)
        #------------------------------------------------------------

        # print("self.store after: ", self.store)
        # print ("self.store.keys() after: ", self.store.keys())
        # print ()
        # print ()

    def remove_mountain(self, mountain: Mountain):
        # Remove a mountain from the manager
        # if str(mountain.difficulty_level) in self.store.keys():
        #     print (type(self.store))
        #     # if mountain.name in self.store
        #     if len(self.store.keys(str(mountain.difficulty_level))) == 1 and mountain in self.store.keys(str(mountain.difficulty_level)):
        #         # del self.store[str(mountain.difficulty_level)]
        #         self.store.values().remove(mountain)
        #     elif mountain in self.store.values():
        #         print (mountain)
        #         print (self.store.values())
        #         # self.store[str(mountain.difficulty_level)] = self.store[str(mountain.difficulty_level)].remove(mountain)
        #         self.store.values().remove(mountain)
        #         # self.store.count -=1
        # print ("------------AKHIR------------")
        # print ("akhir: ", self.store.values())
        # print ("------------------------------")

        if str(mountain.difficulty_level) in self.store.keys():
            # a = self.store.values().remove(mountain)
            # print ("********************************")
            # print ("disini woi",self.store.values(str(mountain.difficulty_level)))
            # print ("********************************")
            # a = self.store.values(str(mountain.difficulty_level))
            del self.store[str(mountain.difficulty_level), mountain.name]

        # try:
        #     del self.store[str(mountain.difficulty_level)]
        # except:
        #     raise KeyError
    def edit_mountain(self, old: Mountain, new: Mountain):
        # Remove the old mountain and add the new mountain.
        self.remove_mountain(old)
        self.add_mountain(new)


    def mountains_with_difficulty(self, diff: int):
        #Return a list of all mountains with this difficulty.
        print ("diff: ", diff)
        # if str(diff) in self.store.keys():
        #     print ("self.store.keys(): ", self.store.keys())
        #     self.mountain_list += (self.store.keys(str(diff)))
        #     print ("aa: ",self.mountain_list)
        #     return self.mountain_list
        # for item in self.store.values(str(diff)):
        #     print (item)
        # if str(diff) in self.store.values(str(diff)):
        #     self.mountain_list += (self.store.values(str(diff)))
        #     print (self.mountain_list)
        #     return self.mountain_list
        try:
            return (self.store.values(str(diff)))
        except:
            return []

    def group_by_difficulty(self):
        # Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        # self.store.values is sorted by the name
        #----------------------------------------
        sorted_list = []
        a = []
        print ("value store: ", self.store.values())
        print()
        #-------------------------------------------
        # name_list = mergesort(self.store.values(),key=lambda x:x.name) #sort the name
        print ("aaaaa",type(self.store.values()))
        # key_list = mergesort(self.store.keys(),key=lambda x:x) #sort the given difficulty level

        # sorted_list = merge(name_list,key_list, key = lambda x:x.difficulty_level)
        # sorted_list = mergesort(self.store.values(), key=lambda x:x.name)
        # print ("sort: ", sorted_list)
        print ("name_list: ", self.store.values())
        print ("key_list: ",self.store.keys())
        # for key in self.store.values():
        #     print ("masuk sini")
        #     print ("ini key: ", key)
        #     # print ("type: ", type(key))
        #     sorted_list +=  self.store.values()
        # print (self.store.key)
        print ("panjang store: ", len(self.store))
        # for i in range (len(self.store))

        #correct:
        # for i in self.store.values():
        #     print ("III: " ,i)
        #     print (i.difficulty_level)
        #     if str(i.difficulty_level) in self.store.keys():
        #         print ("keylist: ", self.store.keys())
        #         # print ("ASDASDAS")
        #         print ("--------------------------")
        #         print ("i yg msk: ", i)
        #         sorted_list.append([i])
                # a.append([i.difficulty_level])

        for i in self.store.keys():
            print ("fasdfasdf; ",self.store.values(i))
            sorted_list += [self.store.values(i)]
        

        
        print ("---------- LIST ------------")
        print ("list: ", sorted_list)
        # print ("a: ", a)
        print ("len sorted: ", len(sorted_list))
        print ("----------------------------")
        #-------------------------------------------
        # return sorted_list

        # for i in range (len(name_list)):
        #     if name_list[i].difficulty_level == key_list[i]:
        #         sorted_list.append(name_list[i])
        # for item in key_list:
        #     if item == str(name_list.keys(item)):
        #         sorted_list += str(name_list.keys(item))
        # for i in name_list:
        #     print ("asdf: ", i.difficulty_level)
        #     print ("i: ", i)
            # if i in key_list:
            #     print ("wow masuk")
                # print ("gg: ", i.difficulty_level)
                # sorted_list.append(i.values())
            
            
        # for key in key_list:
        #     print ("key: ",key)
        #     sorted_list.append(mergesort(self.store.values(key),key=lambda x:x.difficulty_level))
            # sorted_list.append()
        # print ("sorted_list: ", sorted_list)
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
    # print(make_set(res[1]), make_set([m3, m4]))
    # print(make_set(res[2]), make_set([m5]))
    # print(make_set(res[3]), make_set([m6, m7, m8, m9]))

    mm.add_mountain(m10)
    # mm.remove_mountain(m5)

    res = mm.group_by_difficulty()
    # print(len(res), 4)

    # print(make_set(res[3]), make_set([m10]))



