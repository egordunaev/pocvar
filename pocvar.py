import sys
import numpy as np
import cv2
from cv2 import aruco
import sys


class POCVAR():
    def __init__(self,
                 markers=None,
                 images=None,
                 video=None,
                 display_video=True,
                 save_video=False):
        self.marker = read_markers(markers)
        self.image = read_images(images)
        self.video = read_video(video)
        self.display_video = display_video
        self.save_video = save_video

        if self.save_video is True:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            x, y = get_original_dimentions(self.video)
            new_video_path = video.replace(".mp4", "_augmented.avi")
            self.video_edit = cv2.VideoWriter(new_video_path, fourcc, 30.0, (x , y))

    def augment_video(self):
        try:
            total_frames = 0
            while self.video.isOpened():
                success, frame = self.video.read()
                if not success:
                    break
                total_frames += 1
                print(f"Processing frame {total_frames}...")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
                arucoParameters = aruco.DetectorParameters_create()
                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
                if np.all(ids != None):
                    display = aruco.drawDetectedMarkers(frame, corners)
                    x1 = (corners[0][0][0][0], corners[0][0][0][1])
                    x2 = (corners[0][0][1][0], corners[0][0][1][1])
                    x3 = (corners[0][0][2][0], corners[0][0][2][1])
                    x4 = (corners[0][0][3][0], corners[0][0][3][1])

                    im_dst = frame
                    size = self.image.shape
                    pts_dst = np.array([x1, x2, x3, x4])
                    pts_src = np.array([[0, 0], [size[1] - 1, 0], [size[1] - 1, size[0] - 1], [0, size[0] - 1]], dtype=float)

                    h, status = cv2.findHomography(pts_src, pts_dst)
                    temp = cv2.warpPerspective(self.image, h, (im_dst.shape[1], im_dst.shape[0]))
                    cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16)
                    im_dst = im_dst + temp
                    if self.display_video: cv2.imshow("Display", im_dst)
                    if self.save_video: self.video_edit.write(im_dst)
                else:
                    display = frame
                    if self.display_video: cv2.imshow("Display", display)
                    if self.save_video: self.video_edit.write(display)
                if self.display_video: cv2.waitKey()
            print("Finishing...")
            self.video.release()
            self.video_edit.release()
            cv2.destroyAllWindows()
        except Exception as error:
            print(f"An error occured: {error}")

def get_original_dimentions(video):
    success, frame = video.read()
    if success:
        return frame.shape[1], frame.shape[0]
    
def read_markers(marker_path):
    try:
        print(f"Reading marker on {marker_path}...")
        return cv2.imread(marker_path)
    except Exception as error:
        print(f"An error occured: {error}")
    
def read_images(image_path):
    try:
        print(f"Reading replacement image on {image_path}...")
        return cv2.imread(image_path)
    except Exception as error:
            print(f"An error occured: {error}")

def read_video(video_path):
    try:
        print(f"Reading video on {video_path}...")
        return cv2.VideoCapture(video_path)
    except Exception as error:
            print(f"An error occured: {error}")
    

if __name__ == "__main__":
    arguments = sys.argv[1:]
    marker_path, img_path, video_path = "", "", ""
    try:
        if arguments[0] == "-m":
            marker_path = arguments[1]
        if arguments[2] == "-i":
            img_path = arguments[3]
        if arguments[4] == "-v":
            video_path = arguments[5]
        if arguments[6] == "-d":
            if arguments[7] == "True":
                display_video_bool = True
            else: display_video_bool = False
        if arguments[8] == "-s":
            if arguments[9] == "True":
                save_video_bool = True
            else: save_video_bool = False
    except Exception:
        print(f"An error occured parsing your input.")
    pocvar = POCVAR(marker_path, img_path, video_path, display_video=display_video_bool, save_video=save_video_bool)
    pocvar.augment_video()
