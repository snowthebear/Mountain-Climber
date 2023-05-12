from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from typing import TYPE_CHECKING, Union
from data_structures.linked_stack import LinkedStack
import mountain_manager

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail
    

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
    
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""

        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""

        return TrailSeries(mountain, Trail(TrailSeries(self.mountain, self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""

        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
    
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.
        
        Big-O notation: O(n) where n is the length of linked stack or the length of Trail.

        """

        link_stack = LinkedStack()
        store_obj = self.store #to store the object from self.store so it wont skip the whole code.
        
        while store_obj is not None or not link_stack.is_empty(): #O(n)
                
            if isinstance(store_obj, TrailSeries): #O(1)
                personality.add_mountain(store_obj.mountain)
                store_obj = store_obj.following.store

            elif isinstance(store_obj, TrailSplit): #O(1)
                if personality.select_branch(store_obj.path_top, store_obj.path_bottom) == True: #Top walker #O(1)
                    link_stack.push(store_obj.path_follow.store)
                    store_obj = store_obj.path_top.store
                    
                else: #Bottom walker or Lazy walker #O(1)
                    link_stack.push(store_obj.path_follow.store)
                    store_obj = store_obj.path_bottom.store

            if store_obj is None and not link_stack.is_empty(): ## to check if you dont have any branch, it means it goes down
                store_obj = link_stack.pop() #O(1)
            
           
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        #should be O(N) where N is the total number of mountains and branches combined.
        lst = []

        if isinstance (self.store, TrailSeries):
            lst.append(self.store.mountain)
            lst += self.store.following.collect_all_mountains()

        elif isinstance (self.store, TrailSplit):
            lst += self.store.path_top.collect_all_mountains()
            lst += self.store.path_bottom.collect_all_mountains()
            lst +=self.store.path_follow.collect_all_mountains()

        return lst

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        lst = []
        arr = []

        self.length_k_aux(self.store, k, arr, lst)

        return list(filter(lambda arr: len(arr) == k, lst))
    
    def length_k_aux(self, store, k, arr, lst):
            
        follow_path = LinkedStack()
        
        if store is None and len(follow_path) == 0:
            lst.append(arr)

        elif isinstance(store,TrailSeries):
            if len(arr) == 0:
                self.length_k_aux(store.following.store, k, [store.mountain], lst)
            else:
                arr.append(store.mountain)
                self.length_k_aux(store.following.store, k, arr, lst)
        else: #TrailSplit
            follow_path.push(store.path_follow.store)
            self.length_k_aux(store.path_top.store, k, arr.copy(), lst)
            self.length_k_aux(store.path_bottom.store, k, arr.copy(), lst)
            
        
        if not follow_path.is_empty():
            following = follow_path.pop()
            for arr in lst:
                if isinstance(following, TrailSeries) and len(arr) < k:
                    arr.append(following.mountain)
            
            if isinstance(following, TrailSplit):
                bottom = lst.pop()
                top = lst.pop()
                ## to check each trail whether they got the mountain.
                self.length_k_aux(following.path_top.store, k, top.copy(), lst)
                self.length_k_aux(following.path_bottom.store, k, top.copy(), lst)
                self.length_k_aux(following.path_top.store, k, bottom.copy(), lst)
                self.length_k_aux(following.path_bottom.store, k, bottom.copy(), lst)
