# 🚗 Open Driving Vision

An open-source driving vision simulator designed for experimentation and research in autonomous driving perception.

### 🚀 Getting Started

Clone the repository:
```
git clone https://github.com/ben-gunnels/Open-Driving-Vision.git
cd Open-Driving-Vision
```
### 🛠 Configuration

Customize the simulator settings:

Edit the configuration in src/constants/constants.py

Modify the simulator behavior in src/app.py

### ▶️ Run the Simulator

Launch the application from the root directory:
```
python -m src.app
```
### 👀🔭🥽 View the Outputs
Output images are generated in src/outputs/images.
Labels are generated in src/outputs/labels.
Videos are generated in src/outputs/videos. 

### 🎯 Features

### ✔️ Easily configurable driving vision system✔️ Modular & extensible architecture✔️ Open-source and community-driven

### 🚀 Start experimenting today!

### Interacting with this Application
The StreamSimulator class simulates a continuous drive by streaming objects from the horizon to the front of the frame. This can be used to train and test an image segmentation model on a continuous driving experience.
The RandomSimulator class creates frames filled with objects in random locations. This can be used for getting a diverse set of training and testing data. 

Play around with the application's parameters and settings to create a one-of-a-kind driving experience. 

Add or edit roadside objects in /src/generators/RoadSignBuilds and /src/generators/RoadSignGenerator to suit your own vision. 

### Tutorial: Creating a Custom Road Object

To create a custom road object of your own desire, additions need to be made to the following files:
    1. src/generators/RoadSignBuilds.py
    2. src/generators/RoadSignGenerator.py

Navigate to the directory and proceed with the following steps. 

1.  Create a road object in RoadSignBuilds.Builder._get_default_builds by adding a new object to the dictionary. The template from info_sign can be followed closely.
The first two args should be tuples with None values. These values get populated via randomization when each object is created. Give your object a unique name which matches the key. 
The primary color fills the sign or main object that you create. Secondary color fills the pole that holds the sign. Label value is used to identify each object and must be a unique value between 1 and 255 but should ideally follow the previous object. pole_type can be normal, short, double or none. 

```
    "info_sign":{
                    "args": [(None, None), (None, None), self.center, self.bounds],
                    "kwargs": {
                        "name": "info_sign",
                        "primary_color": colors.blue,
                        "secondary_color": colors.silver,
                        "label_value": (22, 23),
                        "pole_type": "normal"
                    }
                },
```

2. Next, the object's build function must be added to the Builder class. 
A new function: build_my_obj defines the base size of the image you create. This will initialize the size that the object takes at the horizon.
Carefully map out the proportions and geometry of your object beforehand. I recommend using 10px = 1unit and creating your shape accordingly. 

As an example the road work sign was constructed as follows. The starting point is usually defined as the horizontal middle of the pole that is placed underneath the sign. 

The road work sign is a basic diamond shape. Each of the sizes that deviate from x or y are multiplied by a scale factor to shrink the starting size. By convention, the object is mapped in a counterclockwise direction from the bottom middle point. 
```
    def build_road_work_sign(self, starting_point: tuple):
            """
                Diamond sign for road work information.
                1.2u wide, 1.2u tall
            """
            x, y = starting_point
            y += 5*SCALE_FACTOR # If object is a sign, it must move down so that the pole sits somewhere in the middle. 
            return (
                (x, y), 
                (x+6*SCALE_FACTOR, y-6*SCALE_FACTOR), 
                (x, y-12*SCALE_FACTOR),
                (x-6*SCALE_FACTOR, y-6*SCALE_FACTOR)
            )

```
3. The object must be added to the RoadSignGenerator.generate_roadsign function. The function created in the previous step should be identified in the functs dict. 

```
    ...
    "mile_marker": self.builder.build_mile_marker(start_sign_point),
    "my_obj": self.builder.build_my_obj(start_sign_point) # Your object
    }

```

4. (Optional)
For an object without a pole, such as a traffic cone, the build function is passed the randomized starting point directly, rather than the middle of the pole.
```
    "traffic_cone": self.builder.build_traffic_cone(initial_placement[1], initial_placement[0]),
```

The logic for drawing the object must consider whether the object spawns on the left or right side so that it is not drawn to overlap with the road (unless that is the intention)

```
    def build_traffic_cone(self, starting_point: tuple, anchor="left"):
            """
                Builds a traffic cone with the starting point being either the left or right bottom corner based on the anchor value. 
            """
            x, y = starting_point
            if anchor == "right":
                return (
                    (x, y), 
                    (x+6*SCALE_FACTOR, y), 
                    (x+6*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                    (x+5*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                    (x+3*SCALE_FACTOR, y-6*SCALE_FACTOR), 
                    (x+1*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                    (x, y-1*SCALE_FACTOR)
                )
            
            elif anchor == "left":
                return (
                    (x-6*SCALE_FACTOR, y), 
                    (x, y), 
                    (x, y-1*SCALE_FACTOR), 
                    (x-1*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                    (x-3*SCALE_FACTOR, y-6*SCALE_FACTOR),
                    (x-5*SCALE_FACTOR, y-1*SCALE_FACTOR), 
                    (x-6*SCALE_FACTOR, y-1*SCALE_FACTOR)
                )

```