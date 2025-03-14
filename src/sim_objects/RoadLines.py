import numpy as np
from .Colors import Colors
from ..const.constants import (SCREEN_HEIGHT, SCREEN_WIDTH, HORIZON_HEIGHT,LEFT_ROAD_LINE_START_HEIGHT1, LEFT_ROAD_LINE_START_HEIGHT2, 
                               LEFT_ROAD_LINE_END_WIDTH, RIGHT_ROAD_LINE_START_WIDTH1, RIGHT_ROAD_LINE_START_WIDTH2, RIGHT_ROAD_LINE_END_WIDTH,
                               )

colors = Colors()

ROAD_LINES = {
    "left" : {
                    "geo": np.array([
                        (0, SCREEN_HEIGHT * LEFT_ROAD_LINE_START_HEIGHT1),   # Wide start
                        (0, SCREEN_HEIGHT * LEFT_ROAD_LINE_START_HEIGHT2),  # Narrow end
                        (SCREEN_WIDTH * LEFT_ROAD_LINE_END_WIDTH, SCREEN_HEIGHT * HORIZON_HEIGHT)  # Slightly offset for taper
                    ], np.int32),
                    "color": colors.white
                },
    "right" :  {
                    "geo": np.array([
                        (SCREEN_WIDTH * RIGHT_ROAD_LINE_START_WIDTH1, SCREEN_HEIGHT),   # Wide start
                        (SCREEN_WIDTH * RIGHT_ROAD_LINE_START_WIDTH2, SCREEN_HEIGHT),  # Narrow end
                        (SCREEN_WIDTH * RIGHT_ROAD_LINE_END_WIDTH, SCREEN_HEIGHT * HORIZON_HEIGHT)  # Slightly offset for taper
                    ], np.int32),
                    "color": colors.white
                },
    "left_grass": { # Fills in the horizon with grass
                    "geo": np.array([
                        (0, SCREEN_HEIGHT * LEFT_ROAD_LINE_START_HEIGHT1),
                        (0, SCREEN_HEIGHT * HORIZON_HEIGHT),
                        (SCREEN_WIDTH * LEFT_ROAD_LINE_END_WIDTH, SCREEN_HEIGHT * HORIZON_HEIGHT),
                    ], np.int32),
                    "color": colors.grass_green
                  },

    "right_grass": { # Fills in the horizon with grass
                    "geo": np.array([
                        (SCREEN_WIDTH *  RIGHT_ROAD_LINE_START_WIDTH2, SCREEN_HEIGHT),
                        (SCREEN_WIDTH, SCREEN_HEIGHT),
                        (SCREEN_WIDTH, SCREEN_HEIGHT * HORIZON_HEIGHT),
                        (SCREEN_WIDTH * RIGHT_ROAD_LINE_END_WIDTH, SCREEN_HEIGHT * HORIZON_HEIGHT),
                    ], np.int32),
                    "color": colors.grass_green
                  }
}