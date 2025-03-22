from .simulator.StreamSimulator import StreamSimulator
from .simulator.RandomizedSimulator import RandomizedSimulator

number_frames = 500
moving_speed = 0.02 # Keep around 0.02
frame_rate = 15
chaos = 2 # Set higher for RandomizedSimulator (0-40), lower for StreamSimulator (0-10)
sim_name = f"stream_chaos_{chaos}"


# Terrain options = grass, sand, rock, clay
sim = StreamSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain="grass")
# sim = RandomizedSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain="grass")

sim.run()