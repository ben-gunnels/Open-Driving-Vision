from .simulator.StreamSimulator import StreamSimulator
from .simulator.RandomizedSimulator import RandomizedSimulator

"""
  Edit these parameters to adjust the driving experience.
  number_frames specifies the number of images produced by the simulator.
  moving_speed specifies the rate at which objects move relative to their perceived size.
  frame_rate determines video playback rate. Higher frame rate results in faster video for a given moving speed.
  chaos is a multiplier that causes more objects to spawn on the screen.
  sim_name defines the video output name for the file. 

  StreamSimulator simulates a continuous driving experience.
  RandomizedSimulator generates random images of roadside objects. This is ideal for training a model on novel images.
"""
import time
# Key parameters
number_frames = 500
moving_speed = 0.02 # Keep around 0.02
frame_rate = 15
chaos = 2 # Set higher for RandomizedSimulator (0-40), lower for StreamSimulator (0-10)
mode = "stream" # or "random"
terrain = "grass" # clay, sand, rock, grass, random
sim_name = f"{mode}_chaos_{chaos}"
video = True

start = time.time()
# Terrain options = grass, sand, rock, clay
if mode == "stream":
    sim = StreamSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain=terrain, video=video)
else:
    sim = RandomizedSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain=terrain, video=video)
if sim:
    sim.run()

print(f"{time.time() - start}s elapsed")