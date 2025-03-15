import cv2
import os
from .const.constants import FRAME_RATE, IMG_OUTPUT_PATH, VIDEO_OUTPUT_PATH

# Image folder path
image_folder = IMG_OUTPUT_PATH


def video_playback(name: str):
    video_filename = os.path.join(VIDEO_OUTPUT_PATH, f"{name}.mp4")  # Specify output path
    # Get image files sorted by name
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

    # Read the first image to get dimensions
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Create a video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_filename, fourcc, FRAME_RATE, (width, height))

    # Add images to video
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()