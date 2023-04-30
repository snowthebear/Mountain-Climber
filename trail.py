from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from typing import TYPE_CHECKING, Union
from data_structures.linked_stack import LinkedStack

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

        # mountain_remove = Trail(TrailSeries(None, self.following)) ##not sure
        return self.following.store

        # raise NotImplementedError()

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
        """Follow a path and add mountains according to a personality."""

        link_stack = LinkedStack()
        store_obj = self.store #to store the object from self.store so it wont skip the whole code.
        
        while store_obj is not None or not link_stack.is_empty():
                
            if isinstance(store_obj, TrailSeries):
                personality.add_mountain(store_obj.mountain)
                store_obj = store_obj.following.store

            elif isinstance(store_obj, TrailSplit):
                if personality.select_branch(store_obj.path_top, store_obj.path_bottom) == True: #Top walker
                    link_stack.push(store_obj.path_follow.store)
                    store_obj = store_obj.path_top.store
                    
                else: #Bottom walker or Lazy walker 
                    link_stack.push(store_obj.path_follow.store)
                    store_obj = store_obj.path_bottom.store

            if store_obj is None and not link_stack.is_empty(): ## to check if you dont have any branch, it means it goes down
                store_obj = link_stack.pop()
            
           
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()


if __name__ == "__main__":
    # t = Trail(TrailSplit(to))
    # print (t.follow_path(TopWalker()))
    pass