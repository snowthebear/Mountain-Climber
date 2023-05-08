from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")

def binary_search(l: list[T], item: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.

    :return: The index at which either:
        * This item is located, or
        * Where this item would be inserted to preserve the ordering.

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    # return (self.rank_list, mountain.name, lo=0, hi= len(self.rank_list))
    # print ("l:", l , ", item: ", item)
    return _binary_search_aux(l, item, 0, len(l))

# def _binary_search_aux(l: list[T], item: T, lo: int, hi: int, i =0) -> int:
#     """
#     Auxilliary method used by binary search.
#     lo: smallest index where the return value could be.
#     hi: largest index where the return value could be.
#     """
#     #(self.rank_list, mountain.name, lo=0, hi= len(self.rank_list)
#     if lo == hi:
#         return lo
   
#     # i +=1
#     if i < len(item.name):
#         mid = (hi + lo) // 2
#         name = l[mid].name
#         if ord(name[i]) != ord(item.name[i]):
#             if ord(name[i]) > ord(item.name[i]):
#                 # Item would be before mid
#                 return _binary_search_aux(l, item, lo, mid,i+1)
#             elif ord(name[i]) < ord(item.name[i]):
#                 # Item would be after mid
#                 print (ord(name[i]), ord(item.name[i]))
#                 # i +=1
#                 return _binary_search_aux(l, item, mid+1, hi,i+1)
    
#             # elif ord(name[i]) == ord(item.name[i]):
#         else:
#             i+=1
#             return _binary_search_aux(l, item, lo, hi ,i)
#     else:
#         raise ValueError
    
    # if lo == hi:
    #         return lo
    #     mid = (hi + lo) // 2
    #     if l[mid].name != item.name:
    #         # print ("AA")
    #         # Item would be before mid
    #         up = _binary_search_aux(l, item, lo, mid)
    #         down = _binary_search_aux(l, item, mid+1, hi)
    #     # elif l[mid].name[1] < item.name:
    #     #     # print ("BB")
    #     #     # Item would be after mid
    #     #     return _binary_search_aux(l, item, mid+1, hi)
    #     elif l[mid].name == item.name:
    #         return mid
    #     raise ValueError(f"Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.")

#--------------------------------------------------------------------
def _binary_search_aux(l: list[T], item: T, lo: int, hi: int) -> int:
    """
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    #(self.rank_list, mountain.name, lo=0, hi= len(self.rank_list)
    print ("--------- START --------")
    if lo == hi:
        # if l[lo] == item:
        #     print ("lo hi")
        return lo #hard code
    mid = (hi + lo) // 2
    print ("mid: ",mid)
    print ("l[mid]: ", l[mid])
    # if l[mid] != item:
    
    if l[mid].length > item.length:
        print ("AA")
        # Item would be before mid
        return _binary_search_aux(l, item, lo, mid)
    elif l[mid].length < item.length:
        print ("BB")
        # Item would be after mid
        return _binary_search_aux(l, item, mid+1, hi)
    
    elif l[mid].length == item.length:
        if l[mid].name == item.name:
            print ("------------GET-------------------------------------")
            return mid
        elif ord(l[mid].name[1]) > ord(item.name[1]):
            print ("maas")
            return _binary_search_aux(l, item, lo, mid)
        # else:
        elif ord(l[mid].name[1]) < ord(item.name[1]):
            print ("omgomg")
            return _binary_search_aux(l, item, mid+1, hi)
            
    # elif l[mid].name == item.name:
    #     print ("------------GET-------------------------------------")
    #     # print ("CC")
    #     return mid
    # else:
    #     print ("---------------MASUK SINI-------------")
    #     print ("list: ", l)
    #     print ("mid: ", mid)
    #     print ("mm: ", (l[mid], item))
    #     print ("lo: ", lo, "hi: ", hi)
    #     # mid = 1
    #     return _binary_search_aux(l, item, mid+1, hi)
    

    raise ValueError(f"Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.")