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
from .video_playback import video_playback
from .const.constants import (SCREEN_HEIGHT, SCREEN_WIDTH, HORIZON_HEIGHT, CENTER, BOUNDS, MEDIAN_LINE_ANGLE,
                               ROAD_LINE_MAX_LENGTH, ROAD_LINE_GAP_MAX_LENGTH, IMG_OUTPUT_PATH, LABELS_OUTPUT_PATH,
                               LEFT_ROAD_LINE_START_HEIGHT1, LEFT_ROAD_LINE_START_HEIGHT2, LEFT_ROAD_LINE_END_WIDTH,
                               RIGHT_ROAD_LINE_START_WIDTH1, RIGHT_ROAD_LINE_START_WIDTH2, RIGHT_ROAD_LINE_END_WIDTH,
                               DEBUG, DURATION
                               )

colors = Colors()
roadsign_generator = RoadSignGenerator(CENTER, BOUNDS)

if not os.path.exists("./src/logs"):
    os.mkdir("./src/logs")

if os.path.exists("./src/logs/app.log"):
    os.remove("./src/logs/app.log")

if not os.path.exists("./src/outputs/images"):
    os.mkdir("./src/outputs/images")

if not os.path.exists("./src/outputs/labels"):
    os.mkdir("./src/outputs/labels")


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

road_signs = ["diamond_warning_sign", 
              "speed_limit_sign", 
              "stop_sign", 
              "small_informational_sign", 
              "large_informational_sign",
              "yield_sign",
              "freeway_sign",
              "traffic_cone"
              ]

sign = "yield_sign"

road_sign = roadsign_generator.generate_roadsign(sign)
imgs = [np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8) for _ in range(DURATION)]
masks = [np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.uint8) for _ in range(DURATION) ]

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

for i in range(DURATION):
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
    road_sign.draw(imgs[i], masks[i])
    road_sign.move(0.03)

    # Name the image and label mask
    img_filename = f"output_{str(i).zfill(3)}.png"
    label_filename = f"label_{str(i).zfill(3)}.png"

    cv2.imwrite(IMG_OUTPUT_PATH + f"\{img_filename}", imgs[i])
    cv2.imwrite(LABELS_OUTPUT_PATH + f"\{img_filename}", masks[i])
    
    head.move(0.06)
    median = head
    j = 0
    for i in range(60):
        median.calculate_next_median()
        logging.info(f"median {j}: {median.start_x} {median.start_y} {median.post_gap}")
        median = median.next 
        j += 1

    head = find_new_head(head)

video_playback(sign)

# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()