import random
from ..const.constants import (PLACEMENT_DEVIATION, MINIMUM_PLACEMENT_DEVIATION)
random.seed()

class RandomPlacementGenerator:
    def __init__(self, left_edge: float, right_edge: float, top_edge: float, bottom_edge: float, anchor="top_left", deviation:float=PLACEMENT_DEVIATION):
        """
            Params: 
                left_edge (float) - sets the leftmost bound for placement.
                right_edge (float) - sets the rightmost bound for placement.
                top_edge (float) - sets the topmost bound for placement.
                bottom_edge (float) - sets the bottommost bound for placement.
                anchor (float) - sets the point of reference to make placement. The placement is at most deviation distance away from anchor.
                deviation (float) - sets the maximum distance away from the anchor as a percentage of the difference between the left and right edge.
        """
        self.left_edge = left_edge
        self.right_edge = right_edge
        self.top_edge = top_edge
        self.bottom_edge = bottom_edge
        self.anchor = anchor
        self.deviation = deviation

    def randomize_placement(self, fixed:bool = False):
        """
            Spawns a roadside object with a random placement within a valid range from the road lines. 
        
        """
        delta_x = self.right_edge - self.left_edge
        dev = max(delta_x * (random.random() % self.deviation), MINIMUM_PLACEMENT_DEVIATION)
        if fixed:
            dev = 0.02
            
        if self.anchor == "top_left":
            # Placement is set relative to the leftmost top point
            return (self.left_edge + dev, self.top_edge)

        elif self.anchor == "top_right":
            # Placement is set relative to the rightmost top point
            return (self.right_edge - dev, self.top_edge)

        elif self.anchor == "bottom_left":
            # Placement is set relative to the leftmost bottom point
            return (self.left_edge + dev, self.bottom_edge)

        elif self.anchor == "bottom_right":
            # Placement is set relative to the rightmost bottom point
            return (self.right_edge - dev, self.bottom_edge)
    