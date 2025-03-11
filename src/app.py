import cv2
import numpy as np
from .road_objects.Median import Median
import time
import sys
import logging

# Configure logging
logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

SCREEN_HEIGHT, SCREEN_WIDTH = 800, 1216
ROAD_LINE_MAX_LENGTH = int(SCREEN_HEIGHT * 0.18)
ROAD_LINE_GAP_MAX_LENGTH  = int(SCREEN_HEIGHT * 0.2232)

MEDIAN_LINE_ANGLE = 63.018

OUTPUT_PATH = ".\src\outputs"

def find_side_length(angle, hyp, func="sin"):
    if func == "sin":
        return int(hyp * np.sin(angle * (np.pi / 180)))
    
    elif func == "cos":
        return int(hyp * np.cos(angle * (np.pi / 180)))
    
def find_hyp(sideA, sideB):
    return int(np.sqrt(sideA * sideA + sideB * sideB))

def median_line_length(x, y):
    """
        Applies a function to a point along the median line to determine its size.
        The apparent size of the line decreases linearly off into the distance. 
        Takes the straight line from the bottom of the screen to the current starting point as its input. 
    
    """
    return int(-0.32 * find_hyp(x, y) + ROAD_LINE_MAX_LENGTH)

def median_gap_length(x, y):
    return int(-0.32 * find_hyp(x, y) + ROAD_LINE_GAP_MAX_LENGTH)
    
road_lines = {
    "left" : {
                    "geo": np.array([
                        (0, int(SCREEN_HEIGHT * 0.87)),   # Wide start
                        (0, int(SCREEN_HEIGHT * 0.88)),  # Narrow end
                        (int(SCREEN_WIDTH * 0.48), int(SCREEN_HEIGHT * 0.45))  # Slightly offset for taper
                    ], np.int32),
                    "color": (255, 255, 255)
                },
    "right" :  {
                    "geo": np.array([
                        (int(SCREEN_WIDTH * 0.86), SCREEN_HEIGHT),   # Wide start
                        (int(SCREEN_WIDTH * 0.87), SCREEN_HEIGHT),  # Narrow end
                        (int(SCREEN_WIDTH * 0.50), int(SCREEN_HEIGHT * 0.45))  # Slightly offset for taper
                    ], np.int32),
                    "color": (255, 255, 255)
                },
    "median" :  { 
                    "geo" : np.array([
                        (int(SCREEN_WIDTH * 0.31), SCREEN_HEIGHT),   # Wide start
                        (int(SCREEN_WIDTH * 0.32), SCREEN_HEIGHT),  # Narrow end
                        (int(SCREEN_WIDTH * 0.49), int(SCREEN_HEIGHT * 0.45))  # Slightly offset for taper
                    ], np.int32),
                    "color": (0, 255, 255)  
                },
}
imgs = [np.ones((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8) * 0 for _ in range(60)]

for img in imgs:
    for line in road_lines:
        if line == "median":
            continue
        
        cv2.fillPoly(img, [road_lines[line]["geo"]], road_lines[line]["color"])  # Fill with white)


def find_new_head(head):
    """
        Sets the new head to be the median that is closest to the origin.
    """
    j = 0
    new_head = 0
    closest_to_origin = sys.maxsize
    median = head
    while median.next:
        distance_to_origin = median.distance_to_origin()
        # Early stopping
        if distance_to_origin > closest_to_origin:
            break

        if distance_to_origin < closest_to_origin:
            closest_to_origin = distance_to_origin
            new_head = j
        median = median.next
        j += 1
    
    median = head
    for i in range(new_head):
        median = median.next

    return median

start_y = SCREEN_HEIGHT
end_y = start_y - find_side_length(MEDIAN_LINE_ANGLE, ROAD_LINE_MAX_LENGTH, func="sin")
start_x = int(SCREEN_WIDTH * 0.31)
end_x = start_x + find_side_length(MEDIAN_LINE_ANGLE, ROAD_LINE_MAX_LENGTH, func="cos")
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