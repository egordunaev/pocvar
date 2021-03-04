import sys
import io
import numpy as np
import cv2 as cv
import sys
import argparse
# from matplotlib import pyplot as plt


class POCVAR():
    def __init__(self, markers = None, images = None, video = None, match_count = 10):
        self.markers = read_markers(markers)
        self.images = read_images(images)
        self.video = read_video(video)
        self.match_count = match_count
    
    def find_and_replace(self):
        pass
    
def read_markers(marker_path):
    try:
        print(f"Reading marker on {marker_path[1:]}...")
        return cv.imread(marker_path)
    except Exception:
        print("No marker.")
    
def read_images(image_path):
    try:
        print(f"Reading replacement image on {image_path[1:]}...")
        return cv.imread(image_path)
    except Exception:
        print("No image.")

def read_video(video_path):
    try:
        print(f"Reading video on {video_path}...")
        return cv.VideoCapture(video_path)
    except Exception:
        print("No video.")
    

if __name__ == "__main__":
    pocvar = POCVAR("./markers/marker.jpg", "./img/img.jpg", "/video/marker-testing.mp4")
    print(f"Pocvar status: marker read: {pocvar.markers.any()}; img read: {pocvar.images.any()}; video read: {bool(pocvar.video)}")
