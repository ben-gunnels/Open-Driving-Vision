import time
import sys
import os
import logging
import cv2
import numpy as np
from .sim_objects.Median import Median
from .sim_objects.Point import Point
from .sim_objects.road_objects.RoadSign import RoadSign
from .generators.RoadSignGenerator import RoadSignGenerator
from .sim_objects.Colors import Colors
from .algorithms.Algorithms import (find_new_head)
from .const.constants import (SCREEN_HEIGHT, SCREEN_WIDTH, HORIZON_HEIGHT, CENTER, BOUNDS, MEDIAN_LINE_ANGLE,
                               ROAD_LINE_MAX_LENGTH, ROAD_LINE_GAP_MAX_LENGTH, OUTPUT_PATH,
                               LEFT_ROAD_LINE_START_HEIGHT1, LEFT_ROAD_LINE_START_HEIGHT2, LEFT_ROAD_LINE_END_WIDTH,
                               RIGHT_ROAD_LINE_START_WIDTH1, RIGHT_ROAD_LINE_START_WIDTH2, RIGHT_ROAD_LINE_END_WIDTH,
                               DEBUG
                               )

colors = Colors()
roadsign_generator = RoadSignGenerator(CENTER, BOUNDS)

if not os.path.exists("./src/logs"):
    os.mkdir("./src/logs")

if os.path.exists("./src/logs/app.log"):
    os.remove("./src/logs/app.log")

# Configure logging
logging.basicConfig(filename="src/logs/app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    
road_lines = {
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

sign_points = [
    (SCREEN_WIDTH * 0.52, SCREEN_HEIGHT * HORIZON_HEIGHT - 17),
    (SCREEN_WIDTH * 0.52 - 5, SCREEN_HEIGHT * HORIZON_HEIGHT - 12),
    (SCREEN_WIDTH * 0.52, SCREEN_HEIGHT * HORIZON_HEIGHT - 7),
    (SCREEN_WIDTH * 0.52 + 5, SCREEN_HEIGHT * HORIZON_HEIGHT - 12),
]

pole_points = [
    (SCREEN_WIDTH * 0.52 - 1, SCREEN_HEIGHT * HORIZON_HEIGHT - 8),
    (SCREEN_WIDTH * 0.52 + 1, SCREEN_HEIGHT * HORIZON_HEIGHT - 8),
    (SCREEN_WIDTH * 0.52 + 1, SCREEN_HEIGHT * HORIZON_HEIGHT + 4),
    (SCREEN_WIDTH * 0.52 - 1, SCREEN_HEIGHT * HORIZON_HEIGHT + 4),
]
road_signs = ["diamond_warning_sign", 
              "speed_limit_sign", 
              "stop_sign", 
              "small_informational_sign", 
              "large_informational_sign",
              "yield_sign",
              "freeway_sign",
              "traffic_cone"
              ]

road_sign = roadsign_generator.generate_roadsign(road_signs[0])
imgs = [np.ones((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8) * 0 for _ in range(60)]

for img in imgs:
    for line in road_lines:
        cv2.fillPoly(img, [road_lines[line]["geo"]], road_lines[line]["color"])  # Fill with white
        if DEBUG:
            cv2.circle(img, (int(CENTER[0]), int(CENTER[1])), radius=3, color=colors.red, thickness=1)

ro = Median(0, 0, CENTER, BOUNDS)

start_y = SCREEN_HEIGHT
end_y = start_y - ro._find_side_length(MEDIAN_LINE_ANGLE, ROAD_LINE_MAX_LENGTH, func="sin")
start_x = int(SCREEN_WIDTH * 0.31)
end_x = start_x + ro._find_side_length(MEDIAN_LINE_ANGLE, ROAD_LINE_MAX_LENGTH, func="cos")
post_gap = ROAD_LINE_GAP_MAX_LENGTH

head = Median(start_x, start_y, CENTER, BOUNDS, pre_gap=ROAD_LINE_GAP_MAX_LENGTH, prev=None)
median = head

for i in range(60):
    median.calculate_next_median()
    median = median.next

for i in range(60):
    logging.info(f"ITERATION: {i}")
    median = head
    while median.next:
        if median.start_y > int(SCREEN_HEIGHT * HORIZON_HEIGHT):
            median.draw(imgs[i])
        median = median.next

    # for j, point in enumerate(points):
    #     # print(f"{j}: {point.x}, {point.y}")
    #     point.draw(imgs[i], i)
    #     point.move(0.1)
    road_sign.draw(imgs[i])
    road_sign.move(0.1)

    cv2.imwrite(OUTPUT_PATH + f"\output_{i}.png", imgs[i])

    head.move(0.4)
    median = head
    j = 0
    for i in range(60):
        median.calculate_next_median()
        logging.info(f"median {j}: {median.start_x} {median.start_y} {median.post_gap}")
        median = median.next 
        j += 1

    head = find_new_head(head)

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()