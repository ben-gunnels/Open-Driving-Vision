import cv2
import numpy as np
from ..Colors import Colors
from ..RoadObject import RoadObject
from ..Point import Point

colors = Colors()

class RoadSign(RoadObject):
    def __init__(self, sign: list, pole: list, center: tuple, bounds: tuple, **kwargs):
        super().__init__(kwargs.get("name", "generic_sign"), center, bounds)
        self.sign_points = []
        self.pole_points = []
        self._initialize_sign_points(sign) # Initialize each of the Points as a point object for a sign
        self._initialize_pole_points(pole) # For the pole attached to the sign
        self.primary_color = kwargs.get("primary_color", colors.red)
        self.secondary_color = kwargs.get("secondary_color", colors.wood_brown)
        self.reverse_sign = kwargs.get("reverse_sign", False)
        self.label_value = kwargs.get("label_value", 255)

    def move(self, rate: float):
        for pt in self.sign_points:
            pt.move(rate)
        
        for pt in self.pole_points:
            pt.move(rate)
    
    def draw(self, img, mask_img):
        """
            Draw the shape of the road object at its current position.
            Saves the main shape as a mask
            Params: img (np array)
        """
        valid = any(self._check_valid_display(pt.x, pt.y) for pt in self.sign_points) or any(self._check_valid_display(pt.x, pt.y) for pt in self.pole_points)

        if not valid:
            return
        
        if self.reverse_sign:
            primary_col = colors.silver if self.name != "traffic_cone" else self.primary_color
            cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], primary_col)  # Fill with red
            self.mask = cv2.fillPoly(mask_img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], self.label_value)  # Fill with red

            if self.name != "traffic_cone":
                cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.pole_points], dtype=np.int32)], self.secondary_color)
        else:
            if self.name != "traffic_cone":
                cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.pole_points], dtype=np.int32)], self.secondary_color)
            cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], self.primary_color)  # Fill with red
            self.mask = cv2.fillPoly(mask_img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], self.label_value)  # Fill with red


    def _initialize_sign_points(self, points):
        """
            Create a point object for each point located on the edge of a road sign.
        """
        for point in points:
            self.sign_points.append(Point(point[0], point[1], "point", self.center, self.bounds))
       

    def _initialize_pole_points(self, points):
        """
            Create a point object for each point located on the corners of a rectangular pole that holds the road sign. 
        """
        for point in points:
            self.pole_points.append(Point(point[0], point[1], "point", self.center, self.bounds))

    

    