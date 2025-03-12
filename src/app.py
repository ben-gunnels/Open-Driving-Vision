import cv2
import numpy as np
from .road_objects.Median import Median
from .road_objects.Point import Point
from .algorithms.Algorithms import (find_new_head)
import time
import sys
import logging

# Configure logging
logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

SCREEN_HEIGHT, SCREEN_WIDTH = 800, 1216
CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
ROAD_LINE_MAX_LENGTH = int(SCREEN_HEIGHT * 0.18)
ROAD_LINE_GAP_MAX_LENGTH  = int(SCREEN_HEIGHT * 0.2232)

MEDIAN_LINE_ANGLE = 63.018
HORIZON_HEIGHT = 0.45

OUTPUT_PATH = ".\src\outputs"
    
road_lines = {
    "left" : {
                    "geo": np.array([
                        (0, SCREEN_HEIGHT * 0.87),   # Wide start
                        (0, SCREEN_HEIGHT * 0.88),  # Narrow end
                        (SCREEN_WIDTH * 0.48, SCREEN_HEIGHT * HORIZON_HEIGHT)  # Slightly offset for taper
                    ], np.int32),
                    "color": (255, 255, 255)
                },
    "right" :  {
                    "geo": np.array([
                        (SCREEN_WIDTH * 0.86, SCREEN_HEIGHT),   # Wide start
                        (SCREEN_WIDTH * 0.87, SCREEN_HEIGHT),  # Narrow end
                        (SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * HORIZON_HEIGHT)  # Slightly offset for taper
                    ], np.int32),
                    "color": (255, 255, 255)
                },
    "median" :  { 
                    "geo" : np.array([
                        (SCREEN_WIDTH * 0.31, SCREEN_HEIGHT),   # Wide start
                        (SCREEN_WIDTH * 0.32, SCREEN_HEIGHT),  # Narrow end
                        (SCREEN_WIDTH * 0.49, SCREEN_HEIGHT * HORIZON_HEIGHT)  # Slightly offset for taper
                    ], np.int32),
                    "color": (0, 255, 255)  
                },
}

points = [
    Point(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.4 - 5, CENTER, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)),
    Point(SCREEN_WIDTH * 0.6 - 5, SCREEN_HEIGHT * 0.4, CENTER, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)),
    Point(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.4 + 5, CENTER, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)),
    Point(SCREEN_WIDTH * 0.6 + 5, SCREEN_HEIGHT * 0.4, CENTER, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)),
]

imgs = [np.ones((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8) * 0 for _ in range(60)]

for img in imgs:
    for line in road_lines:
        if line == "median":
            continue
        
        cv2.fillPoly(img, [road_lines[line]["geo"]], road_lines[line]["color"])  # Fill with white)

        cv2.circle(img, (int(CENTER[0]), int(CENTER[1])), radius=3, color=(255, 255, 255), thickness=1)

ro = Median(0, 0)

start_y = SCREEN_HEIGHT
end_y = start_y - ro._find_side_length(MEDIAN_LINE_ANGLE, ROAD_LINE_MAX_LENGTH, func="sin")
start_x = int(SCREEN_WIDTH * 0.31)
end_x = start_x + ro._find_side_length(MEDIAN_LINE_ANGLE, ROAD_LINE_MAX_LENGTH, func="cos")
post_gap = ROAD_LINE_GAP_MAX_LENGTH

head = Median(start_x, start_y, pre_gap=ROAD_LINE_GAP_MAX_LENGTH, prev=None)
median = head

for i in range(60):
    median.calculate_next_median()
    median = median.next

for i in range(60):
    logging.info(f"ITERATION: {i}")
    median = head
    while median.next:
        if median.start_y > int(SCREEN_HEIGHT * 0.45):
            median.draw(imgs[i])
        median = median.next

    for j, point in enumerate(points):
        # print(f"{j}: {point.x}, {point.y}")
        point.draw(imgs[i], i)
        point.move(0.1)

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