import tensorflow as tf
import os
import numpy as np

from ....src.const.constants import IMG_OUTPUT_PATH, MASKS_OUTPUT_PATH

# Get sorted lists of image and mask file paths
image_paths = sorted([os.path.join(IMG_OUTPUT_PATH, fname) for fname in os.listdir(IMG_OUTPUT_PATH)])
mask_paths = sorted([os.path.join(MASKS_OUTPUT_PATH, fname) for fname in os.listdir(MASKS_OUTPUT_PATH)])

# Create a TensorFlow Dataset
dataset = tf.data.Dataset.from_tensor_slices((image_paths, mask_paths))

# Function to load and preprocess images and masks
def load_and_preprocess(image_path, mask_path):
    # Load image
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)  # Assuming RGB images
    image = tf.image.resize(image, (256, 256))  # Resize as needed
    image = tf.image.convert_image_dtype(image, tf.float32)  # Normalize to [0,1]
    
    # Load mask
    mask = tf.io.read_file(mask_path)
    mask = tf.image.decode_png(mask, channels=1)  # Assuming single-channel mask
    mask = tf.image.resize(mask, (256, 256))  # Resize as needed
    mask = tf.image.convert_image_dtype(mask, tf.float32)  # Normalize to [0,1]

    return image, mask

# Apply preprocessing
dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
dataset = dataset.batch(32).shuffle(100).prefetch(tf.data.AUTOTUNE)