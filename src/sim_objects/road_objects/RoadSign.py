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
        self.pole2_points = []
        # Set the attributes for the class
        self.primary_color = kwargs.get("primary_color", colors.red)
        self.secondary_color = kwargs.get("secondary_color", colors.wood_brown)
        self.reverse_sign = kwargs.get("reverse_sign", False)
        self.label_value = kwargs.get("label_value", 255)
        self.pole_type = kwargs.get("pole_type", "normal")

        self._initialize_sign_points(sign) # Initialize each of the Points as a point object for a sign
        self._initialize_pole_points(pole) # For the pole attached to the sign

    def move(self, rate: float):
        for pt in self.sign_points:
            pt.move(rate)
        
        for pt in self.pole_points:
            pt.move(rate)

        if self.pole_type == "double":
            for pt in self.pole2_points:
                pt.move(rate)
    
    def draw(self, img, mask_img):
        """
            Draw the shape of the road object at its current position.
            Saves the main shape as a mask
            Params: img (np array)
        """
        valid = self.validate()

        if not valid:
            return
        
        if self.reverse_sign:
            primary_col = colors.silver if self.name != "traffic_cone" else self.primary_color
            cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], primary_col)  # Fill with red
            self.mask = cv2.fillPoly(mask_img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], self.label_value[1])  # Fill with label for backward

            if self.name != "traffic_cone":
                cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.pole_points], dtype=np.int32)], self.secondary_color)
                if self.pole_type == "double":
                    cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.pole2_points], dtype=np.int32)], self.secondary_color)
        else:
            if self.name != "traffic_cone":
                cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.pole_points], dtype=np.int32)], self.secondary_color)
                if self.pole_type == "double":
                    cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.pole2_points], dtype=np.int32)], self.secondary_color)
            cv2.fillPoly(img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], self.primary_color)  # Fill with red
            self.mask = cv2.fillPoly(mask_img, [np.array([(int(pt.x), int(pt.y)) for pt in self.sign_points], dtype=np.int32)], self.label_value[0])  # Fill with label for forward

    def validate(self):
        """ 
            Returns whether the object is in view within the frame. 
        """
        return (
                any(self._check_valid_display(pt.x, pt.y) for pt in self.sign_points) 
                or any(self._check_valid_display(pt.x, pt.y) for pt in self.pole_points)
        )
    
    def get_distance_from_center(self):
        """
            Return the distance from the bottom of the object to the center of the screen.
        """    
        return self.pole_points[0].y

    def _initialize_sign_points(self, points):
        """
            Create a point object for each point located on the edge of a road sign.
        """
        self.sign_points = [Point(pt[0], pt[1], "point", self.center, self.bounds) for pt in points]

    def _initialize_pole_points(self, points):
        """
            Create a point object for each point located on the corners of a rectangular pole that holds the road sign. 
            Distinguish between signs with one pole and two poles
        """
        if self.pole_type == "double": # There are 2 poles
            self.pole_points = [Point(pt[0], pt[1], "point", self.center, self.bounds) for pt in points[0]]
            self.pole2_points = [Point(pt[0], pt[1], "point", self.center, self.bounds) for pt in points[1]]
        else:
            self.pole_points = [Point(pt[0], pt[1], "point", self.center, self.bounds) for pt in points]
        

    

    