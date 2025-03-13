import numpy as np

class RoadObject:
    def __init__(self, *args):
        self.name = args[0]
        self.center = args[1]
        self.bounds = args[2]

    def _find_side_length(self, angle: float, hyp: float, func: str ="sin", mode="rad"):
        """
            Finds the length of a side leg given the hypotenuse and the angle. 
        """
        if mode == "deg":
            angle = angle * (np.pi / 180)

        if func == "sin":
            return hyp * np.sin(angle)
        
        elif func == "cos":
            return hyp * np.cos(angle)
        
    def _find_hyp(self, sideA, sideB):
        """
            Finds the hypotenuse given two side lengths. 
        """
        return np.sqrt(sideA * sideA + sideB * sideB)
    
    def _check_valid_display(self, x, y):
        """
            Bounds are (left_x, top_y, right_x, bottom_y)
        """
        if x < self.bounds[0]:
            return False
        
        if x > self.bounds[2]:
            return False
        
        if y < self.bounds[1]:
            return False

        if y > self.bounds[3]:
            return False
        return True