import numpy as np
import cv2

from .RoadObject import RoadObject
from ..const.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, MEDIAN_LINE_ANGLE, MEDIAN_LINE_MAX_LENGTH, MEDIAN_LINE_GAP_MAX_LENGTH)

class Median(RoadObject):
    def __init__(self, *args, **kwargs):
        super().__init__("median", args[2], args[3]) # Median doesn't require bounds or center
        self.start_x = args[0]
        self.start_y = args[1]

        self.pre_gap = kwargs.get("pre_gap", 0) # The gap that comes before a line
        self.post_gap = None

        self.color = kwargs.get("color", (0, 255, 255))

        self.line = None

        self._calculate_median()

        self.prev = kwargs.get("prev", None)
        self.next = None

    def calculate_next_median(self):
        """
            Calculates the starting point for the next median based on the ending point end_x, end_y.
            Calculates the size of the gap needed to space the median lines. 
            Includes the gap used to calculate the next starting point. 
            post_gap becomes pre_gap for the next median
        """
        self.post_gap = max(self._median_gap_length((self.end_x - SCREEN_WIDTH * 0.31), SCREEN_HEIGHT - self.end_y), 1)
        next_start_x = self.end_x + self._find_side_length(MEDIAN_LINE_ANGLE, self.post_gap, "cos", mode="deg")
        next_start_y = self.end_y - self._find_side_length(MEDIAN_LINE_ANGLE, self.post_gap, "sin", mode="deg")

        self.next = Median(next_start_x, next_start_y, self.center, self.bounds, pre_gap=self.post_gap, prev=self)
    
    def move(self, rate: float):
        """
            Move the median line in the desired direction. This function should only be applied to the median at head.
            The next medians should then be recursively calculated using calculate_next_median
            Params: rate (float), forward (bool)
                rate - The percentage of the pregap that should be covered in a move. 
                forward - specifies the direction the car is perceived to be moving.
        """
        move_length = max(rate * self._find_hyp(self.end_x - self.start_x, self.end_y - self.start_y), 1) # Make it necessary to move 1 pixel
        self.start_x -= self._find_side_length(MEDIAN_LINE_ANGLE, move_length, func="cos", mode="deg")
        self.start_y += self._find_side_length(MEDIAN_LINE_ANGLE, move_length, func="sin", mode="deg")
        if self.prev:
            self.pre_gap = self.prev.post_gap
        self._calculate_median()


    def draw(self, img):
        self.line = cv2.line(img, (int(self.start_x), int(self.start_y)), (int(self.end_x), int(self.end_y)), self.color, 3)

    def distance_to_origin(self):
        d1 = abs(self._find_hyp(self.start_x - SCREEN_WIDTH * 0.31, SCREEN_HEIGHT - self.start_y))
        d2 = abs(self._find_hyp(self.end_x - SCREEN_WIDTH * 0.31, SCREEN_HEIGHT - self.end_y))
        return min(d1, d2)
    
    def _calculate_median(self):
        """
            Calculates the ending point for the current median based on the starting point of start_x, start_y. 
        """
        self.line_length = max(self._median_line_length(self.start_x - SCREEN_WIDTH * 0.31, SCREEN_HEIGHT - self.start_y), 1)
        self.end_y = self.start_y - self._find_side_length(MEDIAN_LINE_ANGLE, self.line_length, func="sin", mode="deg")
        self.end_x = self.start_x + self._find_side_length(MEDIAN_LINE_ANGLE, self.line_length, func="cos", mode="deg")

    def _median_line_length(self, x: float, y: float):
        """
            Applies a function to a point along the median line to determine its size.
            The apparent size of the line decreases linearly off into the distance. 
            Takes the straight line from the bottom of the screen to the current starting point as its input. 
        
        """
        return -0.32 * self._find_hyp(x, y) + MEDIAN_LINE_MAX_LENGTH

    def _median_gap_length(self, x: float, y: float):
        """
            Finds the current gap lenght for the median
        """
        return -0.32 * self._find_hyp(x, y) + MEDIAN_LINE_GAP_MAX_LENGTH


# def main():
#     median = Median(0, 0)
#     print(median.name)


# if __name__ == "__main__":
#     main()