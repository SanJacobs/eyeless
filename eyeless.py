#!/usr/bin/env python3

from process import eyeless_render
import glob
try:
    from sjstools import affirmatrue
except ImportError:
    def affirmatrue(input_string):
        if "y" in input_string or "Y" in input_string:
            return True
        else:
            return False

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
