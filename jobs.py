from PIL import Image, ImageDraw, ImageFilter
import face_recognition
import numpy.polynomial.polynomial as poly
import numpy as np
import glob


def redo_check(path):
    frame_count = int(len(glob.glob1(str(path), "frame*.*")))
    if frame_count == 0:
        print("No frames found at directory. Make sure they are named as such: frame00001.png")
        return True
    else:
        return False


def load_sequence(path):

    # Setting default path
    if path is None:
        path = "media/face_input"

    # Counting frames
    frame_count = int(len(glob.glob1(str(path), "frame*.*")))
    print("Total frames counted: " + str(frame_count))
    unpadded_frame_count = list(range(1, int(frame_count + 1)))
    frames = []

    for each_number in unpadded_frame_count:
        frames.append({
            "file": str(path + "/frame" + str("%0*d" % (5, each_number)) + ".png"),
            "scrap": False,
            "left_eye": None,
            "right_eye": None,
        })
        print("Indexed: " + str(frames[each_number-1]["file"]))

    return frames


def subdivision(frame):
    None


def tracker(image):
    None


def interpolator(all_frames, current_frame_index):
    None


if __name__ == "__main__":
    load_sequence(None)
