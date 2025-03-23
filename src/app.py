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

# Key parameters
number_frames = 150
moving_speed = 0.02 # Keep around 0.02
frame_rate = 15
chaos = 35 # Set higher for RandomizedSimulator (0-40), lower for StreamSimulator (0-10)
mode = "random" # or "random"
terrain = "sand" # clay, sand, rock, random
sim_name = f"{mode}_chaos_{chaos}"

# Terrain options = grass, sand, rock, clay
if mode == "stream":
    sim = StreamSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain=terrain)
else:
    sim = RandomizedSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain=terrain)
if sim:
    sim.run()