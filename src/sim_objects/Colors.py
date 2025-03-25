class Colors:
    """
    Predefined color constants in BGR format.
    Note: These colors are defined as (Blue, Green, Red) tuples, 
    which is the default format in OpenCV.
    """

    # Standard Colors
    white  = (255, 255, 255)  # White
    black  = (0, 0, 0)        # Black
    red    = (0, 0, 255)      # Red (BGR)
    green  = (0, 255, 0)      # Green (BGR)
    blue   = (255, 0, 0)      # Blue (BGR)
    yellow = (0, 255, 255)    # Yellow (BGR)
    orange = (0, 165, 255)    # Orange (BGR)
    silver = (211, 211, 211)  # Silver (BGR)
    purple = (128, 0, 128)    # Purple (BGR)
    cyan   = (255, 255, 0)    # Cyan (BGR)
    magenta = (255, 0, 255)   # Magenta (BGR)
    gray   = (128, 128, 128)  # Neutral gray

    # Custom Colors (Natural & Road-Related)
    grass_green = (21, 109, 19)   # Dark green, resembles grass
    deep_forest_green = (10, 50, 20) # Darker shade of green for forests
    wood_brown  = (19, 69, 139)   # Brownish tone, resembles wood
    sand = (128, 178, 194)        # Goldish sand color, resembles sand
    rock = (65, 77, 90)           # Dark brownish gray, resembling rock
    clay = (80, 106, 182)         # Reddish-brown, resembling Earthen clay
    asphalt_gray = (50, 50, 50)   # Dark gray, resembling asphalt
    dirt_brown = (42, 42, 128)    # Brownish color, resembling dirt roads
    water_blue = (200, 100, 0)    # Blueish color, resembling water

    # Road Sign Colors
    orange_rw = (102, 0, 255)  # Sign for upcoming road work
    info_blue = (255, 144, 30) # Standard blue for motorist info signs
    info_brown = (0, 0, 102)   # Sign for state parks
    highway_green = (0, 128, 0) # Green used for highway signs
    regulatory_black = (0, 0, 0) # Black used in regulatory signs
    guide_green = (0, 150, 0)  # Green used for directional/guide signs
    caution_yellow = (0, 220, 220) # Yellow for warning signs
    pedestrian_crossing = (50, 205, 50) # Fluorescent green for pedestrian crossings
    stop_sign_red = (0, 0, 200) # Deep red for stop signs