# Screen and Display Settings
SCREEN_HEIGHT, SCREEN_WIDTH = 800, 1216
BOUNDS = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Horizon and Center Positioning
HORIZON_HEIGHT = 0.45  # Ratio of screen height
CENTER = (0.49 * SCREEN_WIDTH + 3, HORIZON_HEIGHT * SCREEN_HEIGHT - 8)

# Road Line Properties
MEDIAN_LINES_PER_FRAME = 5
MEDIAN_X_START = 0.31
MEDIAN_LINE_ANGLE = 63.018  # Angle of median lines (degrees)
MEDIAN_LINE_MAX_LENGTH = int(SCREEN_HEIGHT * 0.18)
MEDIAN_LINE_GAP_MAX_LENGTH = int(SCREEN_HEIGHT * 0.2232)

# Left Road Line Start and End Positions
LEFT_ROAD_LINE_START_HEIGHT1 = 0.87
LEFT_ROAD_LINE_START_HEIGHT2 = 0.88
LEFT_ROAD_LINE_END_WIDTH = 0.48

# Right Road Line Start and End Positions
RIGHT_ROAD_LINE_START_WIDTH1 = 0.86
RIGHT_ROAD_LINE_START_WIDTH2 = 0.87
RIGHT_ROAD_LINE_END_WIDTH = 0.50

# Placement Settings (for objects on the road)
PLACEMENT_DEVIATION = 0.06  # Maximum placement deviation
MINIMUM_PLACEMENT_DEVIATION = 0.03  # Minimum placement deviation
LEFT_PLACEMENT_PROB = 0.5  # Probability of left-side placement
SCALE_FACTOR = 0.45

# Pole Properties (Minimum size)
MINIMUM_POLE_HEIGHT = 20  # px
MINIMUM_POLE_WIDTH = 2  # px
SIGN_SCALE = 0.75

# Simulation Settings
DURATION = 140  # Total duration of the simulation
FRAME_RATE = 10  # Frames per second
MAX_CHAOS = 100  # Maximum chaos level (likely affects randomization intensity)
REFRACTORY = 10 # Number of frames between objects being placed on a certain side of the road
OBJECT_PLACEMENT_PROB = 0.75 # The probability of placing a road object on any given frame

# Debugging
DEBUG = False  # Enable/disable debug mode

# Output Paths
LOG_PATH = "./src/logs"
IMG_OUTPUT_PATH = "./src/outputs/images"
MASKS_OUTPUT_PATH = "./src/outputs/masks"
VIDEO_OUTPUT_PATH = "./src/outputs/video"
IMAGE_SEGMENTATION_PATH = "./src/outputs/segmented_images"