import random
import cv2 
from .Simulator import Simulator
from ..algorithms.Algorithms import find_new_head
from ..const.constants import (REFRACTORY, OBJECT_PLACEMENT_PROB)

random.seed()
class StreamSimulator(Simulator):
    def __init__(
            self,
            number_frames: int, 
            moving_speed: float, 
            frame_rate: int, 
            chaos: int=2, 
            sim_name: str="stream_test",
            terrain: str = "grass",
            video: bool = False,
        ):
        super().__init__(
            number_frames=number_frames, 
            moving_speed=moving_speed, 
            frame_rate=frame_rate, 
            chaos=chaos, 
            sim_name=sim_name, 
            terrain=terrain,
            video=video
        )

        # Initialize the last frame that an object was placed
        self.recent_left_object = -REFRACTORY - 1
        self.recent_right_object = -REFRACTORY - 1 
   
    def run(self):
        """
            Runs the simulation for the duration specified.
        """
        for i in range(self.number_frames):
            self.log(f"ITERATION: {i}")
    
            if self._place_object(i, "left"):
                self.recent_left_object = i
            
            if self._place_object(i, "right"):
                self.recent_right_object = i
            
            if i %80 == 0:
                self._place_object(i,"right", True)
                self._place_object(i,"left",True)
                

            # Animate and move the objects
            self._animate_road_objects(i)
            self._animate_median(i)
            self._move_medians()

            # Name the image and label mask
            img_filename = f"output_{str(i).zfill(3)}.png"
            mask_filename = f"output_{str(i).zfill(3)}.png"

            cv2.imwrite(self.img_output_path + f"\{img_filename}", self.frames[i])
            cv2.imwrite(self.mask_output_path + f"\{mask_filename}", self.labels[i])

        # After frames have been created, make a timelapse video of them
        self.create_video()

    def _animate_road_objects(self, i: int):
        """
            Animates the valid road objects into the frame and the label.
            Road objects queue is reversed as back objects need to be drawn first
        """
        for r_obj in reversed(self.road_objects): 
            r_obj.draw(self.frames[i], self.labels[i])
            r_obj.move(self.moving_speed)

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
        self.median_head.move(self.moving_speed * 3)
        median = self.median_head
        j = 0
        for i in range(self.number_medians):
            median.calculate_next_median()
            self.log(f"median {j}: {median.start_x} {median.start_y} {median.post_gap}")
            median = median.next 
            j += 1

        self.median_head = find_new_head(self.median_head)


    def _place_object(self, itr: int, side: str, place_mile_marker: bool= False):
        """
            Places a randomized object with chaos * OBJECT_PLACEMENT_PROB.
            Must allow for a refractory period to pass before an object is placed again
            on either the left side of the road or the right side. 
        """
        recent = self.recent_left_object if side == "left" else self.recent_right_object
        if place_mile_marker:
            self.road_objects.append(self.roadsign_generator.generate_roadsign("mile_marker", side))
            return
        if (itr - recent < REFRACTORY):
            return False
        if random.random() < self.chaos * OBJECT_PLACEMENT_PROB:
            sign = random.choice(self.road_object_names)
            # Clean unviewable objects out of the queue first
            self.remove_invalid_objects()
            self.road_objects.append(self.roadsign_generator.generate_roadsign(sign, side))
            return True
        return False