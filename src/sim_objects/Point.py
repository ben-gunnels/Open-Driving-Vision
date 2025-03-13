import cv2
import numpy as np
from .RoadObject import RoadObject

class Point(RoadObject):
    def __init__(self, x: float, y: float, name: str, center: tuple, bounds: tuple):
        super().__init__(name, center, bounds)
        self.x = x
        self.y = y
        self._calculate_distance_from_center()
        self._calculate_angle_from_center()

    def move(self, rate: float):
        """
            Moves the distance from the point to the center by a specified amount. 
        """
        self.distance += self.distance * rate
        self._calculate_x_y()

    def draw(self, img, i):
        if self._check_valid_display(self.x, self.y):
            cv2.circle(img, (int(self.x), int(self.y)), radius=1, color=(0, 0, 255), thickness=-1)

    def _calculate_x_y(self):
        """
            Used after moving a point along the radius from the center. 
            First make a call to move which increases the distance from the center. 
        """
        self.x = self.center[0] + self._find_side_length(self.angle, self.distance, func="cos")
        self.y = self.center[1] - self._find_side_length(self.angle, self.distance, func="sin") 
    
    def _calculate_distance_from_center(self):
        self.distance = self._find_hyp(self._delta_x(), self._delta_y())

    def _calculate_angle_from_center(self):
        self.angle = np.arctan2(self._delta_y(), self._delta_x())  # Range: [-π, π]
        if self.angle < 0:
            self.angle += 2 * np.pi  # Convert to [0, 2π]
            
    def _delta_x(self):
        return self.x - self.center[0]

    def _delta_y(self):
        return self.center[1] - self.y
        

    


