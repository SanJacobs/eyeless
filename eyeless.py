#!/usr/bin/env python3

from process import eyeless_render
import glob
import sys
from os import path

def affirmatrue(input_string):
    if "y" in input_string.lower():
        return True
    else:
        return False

input_argument_format = "eyeless.py face_input_dir render_output_dir (left)eye_input_dir (right_eye_input_dir)"
# Reading input arguments

if len(sys.argv) == 4 or len(sys.argv) == 5:
    print("Reading input-folder argument...")
    input_directory = sys.argv[1]
    print(input_directory)
    
    print("Reading output-folder argument...")
    output_directory = sys.argv[2]
    print(output_directory)
    
    print("Reading eye-directory...")
    left_eye_directory = sys.argv[3]
    right_eye_directory = sys.argv[3]
    
if len(sys.argv) == 5:
    print("Reading right eye directory...")
    right_eye_directory = sys.argv[3]

elif len(sys.argv) > 5 or (len(sys.argv) < 4 and len(sys.argv) > 1):
    print("Wrong amount of input arguments!")
    print("Proper format:")
    print(input_argument_format)

else:
    print("Input filepaths.")
    print("Where is the folder containing the frames of the face?")
    input_directory = input()
    print("")
    
    print("Where is the folder containing the eye animation?")
    left_eye_directory = input()
    right_eye_directory = left_eye_directory
    print("")
    
    print("Where do you want the finished files to go?")
    output_directory = input()
    print("")

# TODO: Check if input arguments are true
# TODO: Separate left and right eye graphics

# Counting frames
face_frames = len(glob.glob1("media/face_input", "frame*.*"))
print("Counted "+str(face_frames)+" frames.")
eye_frames = len(glob.glob1("media/eye_input", "frame*.*"))
print("Counted "+str(eye_frames)+" frames in eye animation.")

current_eye_frame = 1
first_frame = "frame00001.png"

unpadded_frame_count = list(range(1, int(face_frames+1)))
frames = {}
for each_number in unpadded_frame_count:
    frames[str("frame"+str("%0*d" % (5, each_number))+".png")] = ("%0*d" % (5, each_number))

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

    eyeless_render(first_frame, current_eye_frame, testing, subdiv_res, regr_mode, pad_percent, mask_feather)
    testing = not affirmatrue(input("\nIs this result satisfactory? "))
    if testing:
        print("Ok, let's try again...")

reverse_animation = affirmatrue(input("Do you want to reverse the eye animation? "))

print("Great.")

# Rendering

print("\nRendering all frames...")
for every_frame in frames:
    try:
        eyeless_render(every_frame, current_eye_frame, testing, subdiv_res, regr_mode, pad_percent, mask_feather)
        print("Rendered frame: " + every_frame[5:-4] + "/" + str("%0*d" % (5, face_frames)))
    except ValueError:
        print("Could not find face in: "+every_frame)
        None
    except IndexError:
        print("Could not find face in: " + every_frame)
        None

    if reverse_animation:
        if current_eye_frame > 1:
            current_eye_frame -= 1
        else:
            current_eye_frame = eye_frames
    else:
        if current_eye_frame < eye_frames:
            current_eye_frame += 1
        else:
            current_eye_frame = 1
