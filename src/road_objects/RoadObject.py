import numpy as np

class RoadObject:
    def __init__(self, *args):
        self.name = args[0]

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
        if (sideA < 0 != sideB < 0):
            return -np.sqrt(sideA * sideA + sideB * sideB)
        return np.sqrt(sideA * sideA + sideB * sideB)