import tensorflow as tf
import os
import numpy as np
from ....src.const.constants import (IMG_OUTPUT_PATH, MASKS_OUTPUT_PATH, INPUT_SIZE)

class Augment(tf.keras.layers.Layer):
  def __init__(self, seed=42):
    super().__init__()
    # both use the same seed, so they'll make the same random changes.
    self.augment_inputs = tf.keras.layers.RandomFlip(mode="horizontal", seed=seed)
    self.augment_labels = tf.keras.layers.RandomFlip(mode="horizontal", seed=seed)

  def call(self, inputs, labels):
    inputs = self.augment_inputs(inputs)
    labels = self.augment_labels(labels)
    return inputs, labels

class CreateTensorflowDataset:
    def __init__(self, img_path: str=IMG_OUTPUT_PATH, masks_path: str = MASKS_OUTPUT_PATH, batch_size: int=32):
        # Get sorted lists of image and mask file paths
        self.image_paths = sorted([os.path.join(img_path, fname) for fname in os.listdir(img_path)])
        self.mask_paths = sorted([os.path.join(masks_path, fname) for fname in os.listdir(masks_path)])

        # Create a TensorFlow Dataset
        self.dataset = tf.data.Dataset.from_tensor_slices((self.image_paths, self.mask_paths))
        self.batch_size = batch_size

    def get_dataset(self, test: bool = False):
        # Apply preprocessing
        self.dataset = self.dataset.map(self._load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        
        if not test:
            self.dataset = self.dataset.map(Augment())
            self.dataset = self.dataset.batch(self.batch_size).shuffle(100).prefetch(tf.data.AUTOTUNE)
        else:
           self.dataset = self.dataset.batch(self.batch_size).prefetch(tf.data.AUTOTUNE)
        return self.dataset
        
    def _load_and_preprocess(self, image_path, mask_path):
        # Load image
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image, channels=3)  # Assuming RGB images
        image = tf.image.resize(image, (INPUT_SIZE, INPUT_SIZE))  # Resize as needed
        image = tf.image.convert_image_dtype(image, tf.float32)  # Normalize to [0,1]

        # Load mask
        mask = tf.io.read_file(mask_path)
        mask = tf.image.decode_png(mask, channels=1)  # Assuming single-channel mask
        mask = tf.image.resize(mask, (INPUT_SIZE, INPUT_SIZE))  # Resize as needed
        mask = tf.image.convert_image_dtype(mask, tf.float32)  # Normalize to [0,1]

        return image, mask
    