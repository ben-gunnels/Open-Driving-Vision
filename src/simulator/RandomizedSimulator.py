import random
import cv2 
from collections import deque
from .Simulator import Simulator
from ..sim_objects.Point import Point
from ..algorithms.Algorithms import find_new_head
from ..const.constants import (SCREEN_HEIGHT, CENTER, BOUNDS, OBJECT_PLACEMENT_PROB)

class RandomizedSimulator(Simulator):
    def __init__(
            self, 
            number_frames: int, 
            moving_speed: float, 
            frame_rate: int, 
            chaos: int=2, 
            sim_name: str="random_test",
            terrain: str = "random"
        ):
        # Randomize the terrain if set to random
        terrain = random.choice(["grass", "clay", "sand", "rock"]) if terrain == "random" else terrain
        super().__init__(
            number_frames=number_frames, 
            moving_speed=moving_speed, 
            frame_rate=frame_rate, 
            chaos=chaos, 
            sim_name=sim_name, 
            terrain=terrain
        )


    def run(self):
        """
            Runs the simulation for the duration specified.
        """
        for i in range(self.number_frames):
            self.road_objects = deque([]) # Reset the road objects
            self.log(f"ITERATION: {i}")

            self._randomly_place_objects("left")
            self._randomly_place_objects("right")
            # Animate and move the objects
            self._animate_road_objects(i)
            self._animate_median(i)
            self._move_medians()

            # Name the image and label mask
            img_filename = f"output_{str(i).zfill(3)}.png"
            label_filename = f"label_{str(i).zfill(3)}.png"

            cv2.imwrite(self.img_output_path + f"\{img_filename}", self.frames[i])
            cv2.imwrite(self.mask_output_path + f"\{label_filename}", self.labels[i])

        # After frames have been created, make a timelapse video of them
        self.create_video()

    def _animate_road_objects(self, i: int):
        """
            Animates the valid road objects into the frame and the label.
            Road objects queue is reversed as back objects need to be drawn first
        """
        self._sort_road_objects()
        for r_obj in self.road_objects: 
            r_obj.draw(self.frames[i], self.labels[i])

    def _animate_median(self, i: int):
        """
            Draws the median lines at their current position.
        """
        median = self.median_head

        while median.next:
            if median.start_y > int(self.horizon):
                median.draw(self.frames[i])
            median = median.next
    
    def _move_medians(self):
        """
            Moves the medians along their trajectory. 
        """
        self.median_head.move(self.moving_speed * 2)
        median = self.median_head
        j = 0
        for _ in range(self.number_medians):
            median.calculate_next_median()
            self.log(f"median {j}: {median.start_x} {median.start_y} {median.post_gap}")
            median = median.next 
            j += 1

        self.median_head = find_new_head(self.median_head)


    def _randomly_place_objects(self, side: str):
        """
            Places a randomized object with chaos * OBJECT_PLACEMENT_PROB.
            Must allow for a refractory period to pass before an object is placed again
            on either the left side of the road or the right side. 
        """
        # Unconditionally add mile markers
        self._add_mile_markers()

        for i in range(self.chaos):
            if random.random() < self.chaos * OBJECT_PLACEMENT_PROB: # Chance to randomly place an object
                sign = random.choice(self.road_object_names)
                # Clean unviewable objects out of the queue first
                self.remove_invalid_objects()
                sign = self.roadsign_generator.generate_roadsign(sign, side)

                rate = self._calc_move_distance_rate(sign.sign_points[0])
                
                # Move the sign somewhere along its trajectory
                sign.move(rate * random.random())

                self.road_objects.append(sign)

    def _add_mile_markers(self):
        """
            Adds a pair of mile markers in line to the road objects.
        """
        left_mile_marker = self.roadsign_generator.generate_roadsign("mile_marker", "left")
        right_mile_marker = self.roadsign_generator.generate_roadsign("mile_marker", "right")
        rand_rate = random.random()
        left_mv = self._calc_move_distance_rate(left_mile_marker.sign_points[0])
        right_mv = self._calc_move_distance_rate(right_mile_marker.sign_points[0])
        left_mile_marker.move(left_mv*rand_rate)
        right_mile_marker.move(right_mv*rand_rate)
        self.road_objects.append(left_mile_marker)
        self.road_objects.append(right_mile_marker)


    def _calc_move_distance_rate(self, point: Point):
        """
            Calculates the distance to move a road object along its path.
            Pick any point in the object to calculate the distance
            y
            |\
            | \
            |  \ Max distance
            |___\
        """
        # Get the distance from the object to the bottom of the screen
        bottom_point_y = SCREEN_HEIGHT - point.y
        # Create a point object to calculate the hypotenuse 
        bottom_point = Point(0, bottom_point_y, "bottom_point", CENTER, BOUNDS)
        current_distance = point.distance
        max_distance = bottom_point._find_hyp_side_angle(bottom_point_y, point.angle, func="sin")
        return abs(max_distance / current_distance)
    

    def _sort_road_objects(self):
        """
            Sorts the road objects by y value. 
        """
        self.road_objects = list(self.road_objects)

        self.road_objects.sort(key=lambda x: x.get_distance_from_center())

