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
                    "label_value": (1, 2),
                    "pole_type": "normal"
                }
            },
            "speed_limit_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "speed_limit_sign",
                    "primary_color": colors.white,
                    "secondary_color": colors.silver,
                    "label_value": (3, 4),
                    "pole_type": "normal"
                }
            },
            "stop_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "stop_sign",
                    "primary_color": colors.red,
                    "secondary_color": colors.wood_brown,
                    "label_value": (5, 6),
                    "pole_type": "normal"
                }
            },
            "small_informational_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "small_informational_sign",
                    "primary_color": colors.green,
                    "secondary_color": colors.silver,
                    "label_value": (7, 8),
                    "pole_type": "normal"
                }
            },
            "large_informational_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "large_informational_sign",
                    "primary_color": colors.green,
                    "secondary_color": colors.silver,
                    "label_value": (9, 10),
                    "pole_type": "double"
                }
            },
            "yield_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "yield_sign",
                    "primary_color": colors.red,
                    "secondary_color": colors.wood_brown,
                    "label_value": (11, 12),
                    "pole_type": "normal"
                }
            },
            "freeway_sign": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "freeway_sign",
                    "primary_color": colors.blue,
                    "secondary_color": colors.silver,
                    "label_value": (13, 14),
                    "pole_type": "normal"
                }
            },
            "traffic_cone": {
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "traffic_cone",
                    "primary_color": colors.orange,
                    "secondary_color": colors.white,
                    "label_value": (15, 16), # Should be changed to just 1 label
                    "pole_type": "normal"
                }
            },
            "mile_marker":{
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "mile_marker",
                    "primary_color": colors.green,
                    "secondary_color": colors.silver,
                    "label_value": (17, 18),
                    "pole_type": "short"
                }
            },
            "road_work_sign":{
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "road_work_sign",
                    "primary_color": colors.orange,
                    "secondary_color": colors.silver,
                    "label_value": (19, 20),
                    "pole_type": "normal"
                }
            },
            "tourist_help_sign":{
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "tourist_help_sign",
                    "primary_color": colors.info_brown,
                    "secondary_color": colors.silver,
                    "label_value": (21, 22),
                    "pole_type": "double"
                }
            },
            "info_sign":{
                "args": [(None, None), (None, None), self.center, self.bounds],
                "kwargs": {
                    "name": "info_sign",
                    "primary_color": colors.blue,
                    "secondary_color": colors.silver,
                    "label_value": (23, 24),
                    "pole_type": "normal"
                }
            },
            
        }
    """
        The following functions build the shape of the roadside objects.
    """

    def build_pole(self, starting_point: tuple, pole_type: str="normal", anchor="None"):
        """
            Builds the pole of a sign with the bottom left point of the pole corresponding to the starting point.
        """
        if pole_type == "double":
            return self._build_double_pole(starting_point, anchor)
        
        elif pole_type == "short":
            return self._build_short_pole(starting_point)

        x, y = starting_point

        return (
            (x, y), 
            (x+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y), 
            (x+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR), 
            (x, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR)
        )
    
    def _build_double_pole(self, starting_point: tuple, anchor: str="left"):
        """ 
            Builds a double pole for signs that require them.
            Signs that are compatible with the double pole points are 1.5u wide.
        """
        x, y = starting_point
        
        if anchor == "left":
            return [
                ((x-4, y), 
                (x-4-MINIMUM_POLE_WIDTH*SCALE_FACTOR, y), 
                (x-4-MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR), 
                (x-4, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR)),
                ((x-11, y), 
                (x-11-MINIMUM_POLE_WIDTH*SCALE_FACTOR, y), 
                (x-11-MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR), 
                (x-11, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR))
            ]
        else:
            return [
                ((x+4, y), 
                (x+4+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y), 
                (x+4+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR), 
                (x+4, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR)),
                ((x+11, y), 
                (x+11+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y), 
                (x+11+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR), 
                (x+11, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR))
            ]

    
    def _build_short_pole(self, starting_point: tuple):
        """
            Reduced height of a pole for shorter objects e.g. mile marker.
        """
        x,y = starting_point
        return (
            (x, y),
            (x+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y),
            (x+MINIMUM_POLE_WIDTH*SCALE_FACTOR, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR*.5), 
            (x, y-MINIMUM_POLE_HEIGHT*SCALE_FACTOR*.5)
        )
    
    def build_mile_marker(self, starting_point: tuple):
        """
            Builds a rectangular mile marker topper. 
            1u wide, 0.8u tall
        """
        x, y = starting_point
        # y += 5*SCALE_FACTOR
        return (
            (x+1*SCALE_FACTOR, y), 
            (x+1*SCALE_FACTOR, y-6*SCALE_FACTOR), 
            (x-1*SCALE_FACTOR, y-6*SCALE_FACTOR),
            (x-1*SCALE_FACTOR, y)
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
        y += 5*SCALE_FACTOR
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
    
    def build_tourist_help_sign(self, starting_point: tuple):
        """
            Rectangular sign for tourist help information.
            1.5u wide, 1.4u tall
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x+15*SCALE_FACTOR, y), 
            (x+15*SCALE_FACTOR, y-14*SCALE_FACTOR),
            (x-15*SCALE_FACTOR, y-14*SCALE_FACTOR), 
            (x-15*SCALE_FACTOR, y)
        )  
    
    def build_info_sign(self, starting_point: tuple):
        """
            Rectangular information sign.
            1.2u wide, 1.1u tall

        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x+12*SCALE_FACTOR, y), 
            (x+12*SCALE_FACTOR, y-11*SCALE_FACTOR),
            (x-12*SCALE_FACTOR, y-11*SCALE_FACTOR), 
            (x-12*SCALE_FACTOR, y)
        )
    
    def build_road_work_sign(self, starting_point: tuple):
        """
            Diamond sign for road work information.
            1.2u wide, 1.2u tall
        """
        x, y = starting_point
        y += 5*SCALE_FACTOR
        return (
            (x, y), 
            (x+6*SCALE_FACTOR, y-6*SCALE_FACTOR), 
            (x, y-12*SCALE_FACTOR),
            (x-6*SCALE_FACTOR, y-6*SCALE_FACTOR)
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
    


