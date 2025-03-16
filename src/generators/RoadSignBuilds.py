from ..const.constants import (MINIMUM_POLE_HEIGHT, MINIMUM_POLE_WIDTH, SCALE_FACTOR)
from ..sim_objects.Colors import Colors

colors = Colors()

class Builder():
    def __init__(self, center: tuple, bounds: tuple):
        self.center = center
        self.bounds = bounds
        self._get_default_builds()

    def _get_default_builds(self):
        self.builds = {
            "diamond_warning_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "diamond_warning_sign",
                    "primary_color": colors.yellow,
                    "secondary_color": colors.wood_brown,
                    "label_value": (200, 201)
                }
            },
            "speed_limit_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "speed_limit_sign",
                    "primary_color": colors.white,
                    "secondary_color": colors.silver,
                    "label_value": (202, 203)
                }
            },
            "stop_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "stop_sign",
                    "primary_color": colors.red,
                    "secondary_color": colors.wood_brown,
                    "label_value": (204, 205)
                }
            },
            "small_informational_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "small_informational_sign",
                    "primary_color": colors.green,
                    "secondary_color": colors.silver,
                    "label_value": (206, 207)
                }
            },
            "large_informational_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "large_informational_sign",
                    "primary_color": colors.green,
                    "secondary_color": colors.silver,
                    "label_value": (208, 209)
                }
            },
            "yield_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "yield_sign",
                    "primary_color": colors.red,
                    "secondary_color": colors.wood_brown,
                    "label_value": (210, 211)
                }
            },
            "freeway_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "freeway_sign",
                    "primary_color": colors.blue,
                    "secondary_color": colors.silver,
                    "label_value": (212, 213)
                }
            },
            "traffic_cone": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "traffic_cone",
                    "primary_color": colors.orange,
                    "secondary_color": colors.white,
                    "label_value": (214, 215)
                }
            },
        }
    """
        The following functions build the shape of the roadside objects.
    """

    def build_pole(self, starting_point: tuple):
        """
            Builds the pole of a sign with the bottom left point of the pole corresponding to the starting point.
        """
        x, y = starting_point
        return (
            (x, y), 
            (x+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y), 
            (x+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR), 
            (x, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR)
        )

    
    def build_diamond_sign(self, starting_point: tuple):
        """
            Builds a diamond sign shape from a starting point which is the middle of the top of the sign pole.
            1u wide, 1u tall
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x, y), 
            (x+5*SCALE_FACTOR, y-5*SCALE_FACTOR), 
            (x, y-10*SCALE_FACTOR),
            (x-5*SCALE_FACTOR, y-5*SCALE_FACTOR)
        )

    def build_speed_limit_sign(self, starting_point: tuple):
        """
            Builds a speed limit sign shape from a starting point which is the middle of the top of the sign pole.
            1u wide, 1u tall
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x+5*SCALE_FACTOR, y), 
            (x+5*SCALE_FACTOR, y-10*SCALE_FACTOR), 
            (x-5*SCALE_FACTOR, y-10*SCALE_FACTOR), 
            (x-5*SCALE_FACTOR, y)
        )
    
    def build_stop_sign(self, starting_point: tuple):
        """
            Builds a stop sign shape from a starting point which is the middle of the top of the sign pole.
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR  # Scale the offset
        return (
            (x + 3 * SCALE_FACTOR, y),
            (x + 7.2 * SCALE_FACTOR, y - 4.2 * SCALE_FACTOR),
            (x + 7.2 * SCALE_FACTOR, y - 10.2 * SCALE_FACTOR),
            (x + 3 * SCALE_FACTOR, y - 14.4 * SCALE_FACTOR),
            (x - 3 * SCALE_FACTOR, y - 14.4 * SCALE_FACTOR),
            (x - 7.2 * SCALE_FACTOR, y - 10.2 * SCALE_FACTOR),
            (x - 7.2 * SCALE_FACTOR, y - 4.2 * SCALE_FACTOR),
            (x - 3 * SCALE_FACTOR, y)
        )

    def build_small_informational_sign(self, starting_point: tuple):
        """
            Builds a small informational sign shape from a starting point which is the middle of the top of the sign pole.
            0.6u wide, 1u tall
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x+3*SCALE_FACTOR, y), 
            (x+3*SCALE_FACTOR, y-10*SCALE_FACTOR), 
            (x-3*SCALE_FACTOR, y-10*SCALE_FACTOR),
            (x-3*SCALE_FACTOR, y)
        )
    
    def build_large_informational_sign(self, starting_point: tuple):
        """
            Builds a large informational sign shape from a starting point which is the middle of the top of the sign pole.
            3u wide, 1.6u high
        """
        x, y = starting_point
        y += 5
        return (
            (x+15*SCALE_FACTOR, y), 
            (x+15*SCALE_FACTOR, y-16*SCALE_FACTOR),
            (x-15*SCALE_FACTOR, y-16*SCALE_FACTOR), 
            (x-15*SCALE_FACTOR, y)
        )
    
    def build_yield_sign(self, starting_point: tuple):
        """
            Builds a yield sign shape from a starting point which is the middle of the top of the sign pole.
            Shape is a point side down equilateral triangle.
            Side lengths of 1u
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x, y), 
            (x+3.5*SCALE_FACTOR, y-6.062*SCALE_FACTOR), 
            (x-3.5*SCALE_FACTOR, y-6.062*SCALE_FACTOR)
        )
    
    def build_freeway_sign(self, starting_point: tuple):
        """
            Builds a freeway sign shape from a starting point which is the middle of the top of the sign pole.
            Shape is a point side down pentagon.
            Side lengths of 0.8u
        """
        x, y = starting_point
        y += 5
        return (
            (x, y), 
            (x+6.5*SCALE_FACTOR, y-4.7*SCALE_FACTOR), 
            (x+1.8*SCALE_FACTOR, y-11.2*SCALE_FACTOR), 
            (x-1.8*SCALE_FACTOR, y-11.2*SCALE_FACTOR), 
            (x-6.5*SCALE_FACTOR, y-4.7*SCALE_FACTOR)
        )
    
    def build_traffic_cone(self, starting_point: tuple, anchor="left"):
        """
            Builds a traffic cone with the starting point being either the left or right bottom corner based on the anchor value. 
        """
        x, y = starting_point
        if anchor == "right":
            return (
                (x, y), 
                (x+6*SCALE_FACTOR, y), 
                (x+6*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                (x+5*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                (x+3*SCALE_FACTOR, y-6*SCALE_FACTOR), 
                (x+1*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                (x, y-1*SCALE_FACTOR)
            )
        
        elif anchor == "left":
            return (
                (x-6*SCALE_FACTOR, y), 
                (x, y), 
                (x, y-1*SCALE_FACTOR), 
                (x-1*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                (x-3*SCALE_FACTOR, y-6*SCALE_FACTOR),
                (x-5*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                (x-6*SCALE_FACTOR, y-1*SCALE_FACTOR)
            )
    


