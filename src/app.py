from .simulator.StreamSimulator import StreamSimulator
from .simulator.RandomizedSimulator import RandomizedSimulator

number_frames = 100
moving_speed = 0.02
frame_rate = 10
chaos = 7
sim_name = f"stream_chaos{chaos}"


# Terrain options = grass, sand, rock, clay
sim = StreamSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain="sand")
# sim = RandomizedSimulator(number_frames=number_frames, moving_speed=moving_speed, frame_rate=frame_rate, chaos=chaos, sim_name=sim_name, terrain="clay")

sim.run()