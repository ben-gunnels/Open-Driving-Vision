from .simulator.StreamSimulator import StreamSimulator
from .simulator.RandomizedSimulator import RandomizedSimulator

number_frames = 600
moving_speed = 0.02 # Keep around 0.02
frame_rate = 15
chaos = 1 # Set higher for RandomizedSimulator (0-40), lower for StreamSimulator (0-10)
mode = "stream" # or "random"
terrain = "grass"
sim_name = f"{mode}_chaos_{chaos}"

# Terrain options = grass, sand, rock, clay
if mode == "stream":
    sim = StreamSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain=terrain)

elif mode == "random":
    sim = RandomizedSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain=terrain)

if sim:
    sim.run()