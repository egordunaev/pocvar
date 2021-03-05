# **POCVAR**
Python Open Source Computer Vision Library for Augmented Reality (POCVAR)

This project is made and tested on `python 3.7.3`

# Usage

To run this program simply run:

`python -m <path to your marker> -i <path to replacement image> -v <path to video> -d <Display video? True/False> -s <Save video? True/False>`

## Notes: 
> Augmented video is saved in the same folder where original video is stored, but with `_augmented` mark.

> By default `pocvar.py` will display augmented video, but will **not** save it.

# Example

You can run `python -m markers/5.jpg -i img/img.jpg -v video/aruco_markers.mp4 -d True -s True`
