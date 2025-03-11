import numpy as np

class RoadObject:
    def __init__(self, *args):
        self.name = args[0]

    def _find_side_length(self, angle: float, hyp: float, func: str ="sin"):
        """
            Finds the length of a side leg givent the hypotenuse and the angle. 
        
        """
        if func == "sin":
            return hyp * np.sin(angle * (np.pi / 180))
        
        elif func == "cos":
            return hyp * np.cos(angle * (np.pi / 180))
        
    def _find_hyp(self, sideA, sideB):
        """
            Finds the hypotenuse given two side lengths. 
        """
        if (sideA < 0 != sideB < 0):
            return -np.sqrt(sideA * sideA + sideB * sideB)
        return np.sqrt(sideA * sideA + sideB * sideB)