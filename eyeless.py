#!/usr/bin/env python3

# NOTE: Doesn't work right now, see line 111

# TODO: Make it file name agnostic
# TODO: Just overwrite the previous line during rendering unless something went wrong
# TODO: Progress bar
# TODO: Ask if untracked frames should be skipped or go unrendered
# TODO: Duplicate file handling
# TODO: Separate left and right eye graphics
# TODO: [Wishful] Graph amount of change between frames for the user to be able to catch any glitched frames, and let the user overwrite those frames with an interpolation of the frame before and after it

from process import eyeless_render
import glob
import sys
from os import path

def affirmatrue(input_string):
    return "y" in input_string.lower():

input_argument_format = "eyeless.py face_input_dir render_output_dir (left)eye_input_dir (right_eye_input_dir)"

properly_argumented = False
input_directory = ""
left_eye_directory = ""
right_eye_directory = ""
output_directory = ""

# Reading input arguments

if len(sys.argv) == 4 or len(sys.argv) == 5:
    
    print("Reading input-folder argument...")
    input_directory = sys.argv[1]
    if not input_directory.endswith("/"):
        input_directory += "/"
    print(input_directory)
    
    print("Reading output-folder argument...")
    output_directory = sys.argv[2]
    if not output_directory.endswith("/"):
        output_directory += "/"
    print(output_directory)
    
    print("Reading eye-directory...")
    left_eye_directory = sys.argv[3]
    right_eye_directory = sys.argv[3]
    if not left_eye_directory.endswith("/"):
        left_eye_directory += "/"
    if not right_eye_directory.endswith("/"):
        right_eye_directory += "/"
    
if len(sys.argv) == 5:
    print("Reading right eye directory...")
    right_eye_directory = sys.argv[3]

elif len(sys.argv) > 5 or (len(sys.argv) < 4 and len(sys.argv) > 1):
    print("Wrong amount of input arguments!")
    print("Proper format:")
    print(input_argument_format)
    sys.exit()

# Runtime path input and verification
while not path.isdir(input_directory):
    print("Input filepaths.")
    print("Where is the folder containing the frames of the face?")
    input_directory = input()
    print("")

while not path.isdir(left_eye_directory):
    print("Where is the folder containing the eye animation?")
    left_eye_directory = input()
    right_eye_directory = left_eye_directory
    print("")

while not path.isdir(output_directory):
    print("Where do you want the finished files to go?")
    output_directory = input()
    print("")


# Loading input frames
frames = glob.glob(str(input_directory+"*.*"))
frames.sort()
eye_frames = glob.glob(str(left_eye_directory+"*.*"))
eye_frames.sort()

# Counting frames
face_frame_count = len(frames)
print("Counted "+str(face_frame_count)+" frames.")
eye_frame_count = len(eye_frames)
print("Counted "+str(eye_frame_count)+" frames in eye animation.")

current_eye_frame = 1
first_frame = frames[0]

print("\nEngaging preview using: "+first_frame)

# Testing settings phase

testing = True
while testing:
    subdiv_res = int(input("\nInput subdivision resolution for eyes (1 to disable): "))

    if subdiv_res != 1:
        regr_mode = int(input("Input regression mode (3 for quadratic, 4 for cubic): "))
    else:
        regr_mode = 3

    pad_percent = float(int(input("Input padding percentage: %"))/100)
    mask_feather = int(input("Input mask feathering amount: "))

    # FIXME: Currently this doesn't work at all because current_eye_frame sends a number, but eyeless_render() doesn't have the ability to reconstruct the filepath from just a number
    eyeless_render(first_frame, current_eye_frame, testing, subdiv_res, regr_mode, pad_percent, mask_feather)
    testing = not affirmatrue(input("\nIs this result satisfactory? "))
    if testing:
        print("Ok, let's try again...")

reverse_animation = affirmatrue(input("Do you want to reverse the eye animation? "))

print("Great.")

# Rendering
# TODO: Only print text on NEW line when error occured, otherwise, overwrite previous line

current_frame_nr = 1
print("\nRendering all frames...")
for each_frame in frames:
    try:
        eyeless_render(each_frame, current_eye_frame, testing, subdiv_res, regr_mode, pad_percent, mask_feather)
        print("Rendered frame: " + str(current_frame_nr) + "/" + str(face_frame_count))
    except ValueError:
        print("Could not find face in: " + each_frame)
        None
    except IndexError:
        print("Could not find face in: " + each_frame)
        None

    if reverse_animation:
        if current_eye_frame > 1:
            current_eye_frame -= 1
        else:
            current_eye_frame = eye_frame_count
    else:
        if current_eye_frame < eye_frame_count:
            current_eye_frame += 1
        else:
            current_eye_frame = 1
    #FIXME: Stupid repeated comparison, just use modulo
