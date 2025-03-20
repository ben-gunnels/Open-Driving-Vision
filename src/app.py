from .simulator.StreamSimulator import StreamSimulator
from .simulator.RandomizedSimulator import RandomizedSimulator

number_frames = 500
moving_speed = 0.02 # Keep around 0.02
frame_rate = 15
chaos = 25 # Set higher for RandomizedSimulator
sim_name = f"random_chaos_{chaos}"


# Terrain options = grass, sand, rock, clay
# sim = StreamSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain="clay")
sim = RandomizedSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain="clay")

sim.run()