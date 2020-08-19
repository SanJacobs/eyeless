#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFilter
import face_recognition
import numpy.polynomial.polynomial as poly
import numpy as np

# Default values
# subdiv_res = 8
# regr_mode = 3
# pad_percent = 0.3
# mask_feather = 1


def eyeless_render(__frame, __framenr, __testing, subdiv_res, regr_mode, pad_percent, mask_feather):
    #print("Loading "+__frame+"...")
    input_image = face_recognition.load_image_file("media/face_input/"+__frame)

    #print("Reading face...")
    face_landmark_list = face_recognition.face_landmarks(input_image)



    # Setting up coordinate splits for each eye's coordinates
    # Naming convention: Left/right, X/Y, top/bottom.
    splits_dict = {"lxt": [],
                   "lyt": [],
                   "lxb": [],
                   "lyb": [],

                   "rxt": [],
                   "ryt": [],
                   "rxb": [],
                   "ryb": []}


    for each_landmark in face_landmark_list:

        # Parsing coordinates out of polygons and into numpy arrays.
        # Left eye:
        # Top half
        #print("Top left:")
        for each_coordinate in each_landmark["left_eye"][:4]:
            #print(each_coordinate)
            splits_dict["lxt"].append(each_coordinate[0])
            splits_dict["lyt"].append(each_coordinate[1])
        # Putting first coordinate at end, so both top and bottom coordinate lists contain final point.
        each_landmark["left_eye"].append(each_landmark["left_eye"][0])
        #print("Bottom left:")
        for each_coordinate in each_landmark["left_eye"][3:]:
            #print(each_coordinate)
            splits_dict["lxb"].append(each_coordinate[0])
            splits_dict["lyb"].append(each_coordinate[1])

        # Right eye:
        # Top half
        #print("\nTop right:")
        for each_coordinate in each_landmark["right_eye"][:4]:
            #print(each_coordinate)
            splits_dict["rxt"].append(each_coordinate[0])
            splits_dict["ryt"].append(each_coordinate[1])
        # Putting first coordinate at end, so both top and bottom coordinate lists contain final point.
        each_landmark["right_eye"].append(each_landmark["right_eye"][0])
        #print("Bottom right:")
        for each_coordinate in each_landmark["right_eye"][3:]:
            #print(each_coordinate)
            splits_dict["rxb"].append(each_coordinate[0])
            splits_dict["ryb"].append(each_coordinate[1])


    # Grabbing placement coordinates before subdivision because it's simpler.
    #print("Calculating left eye dimensions...")
    left_eye_width = int(splits_dict["lxt"][-1] - splits_dict["lxt"][0])
    left_eye_true_center = (int(round(int(splits_dict["lxt"][1]+splits_dict["lxt"][2]+splits_dict["lxb"][1]+splits_dict["lxb"][2])/4, 0)),
                            int(round(int(splits_dict["lyt"][1]+splits_dict["lyt"][2]+splits_dict["lyb"][2]+splits_dict["lyb"][2])/4, 0)))

    #print("Calculating right eye dimensions...")
    right_eye_width = int(splits_dict["rxt"][-1] - splits_dict["rxt"][0])
    right_eye_true_center = (int(round(int(splits_dict["rxt"][1]+splits_dict["rxt"][2]+splits_dict["rxb"][1]+splits_dict["rxb"][2])/4, 0)),
                             int(round(int(splits_dict["ryt"][1]+splits_dict["ryt"][2]+splits_dict["ryb"][2]+splits_dict["ryb"][2])/4, 0)))

    # Super-sampling the quadratic regression for subdivision vertices


    def subdivision(split):

        #print("\nSubdividing "+split+"...")

        x_calc = np.array(splits_dict[str(split[0]+"x"+split[-1])])
        y_calc = np.array(splits_dict[str(split[0]+"y"+split[-1])])

        # Doing the actual regression
        x_new = np.linspace(x_calc[0], x_calc[-1], num=len(x_calc)*subdiv_res)
        coefs = poly.polyfit(x_calc, y_calc, regr_mode)
        y_new = poly.polyval(x_new, coefs)

        #print(x_new)
        #print(y_new)

        # Putting the new coordinates back into the splits dictionary, now that they're up-scaled
        splits_dict[str(split[0]+"x"+split[-1])] = list(x_new)
        splits_dict[str(split[0] + "y" + split[-1])] = list(y_new)

        if "b" in split:
            del splits_dict[str(split[0] + "x" + split[-1])][-1]
            del splits_dict[str(split[0] + "y" + split[-1])][-1]

        return


    fused_splits = {}

    # Executing the subdivisions and ZIPing coordinates back into a 2D list.
    # Since PIL takes lists formatted as such for polygons: [(X, Y), (X, Y), (X, Y), (X, Y)]
    for each_split_name, each_split in splits_dict.items():
        working_split = str(each_split_name[::2])
        if "x" in each_split_name:
            subdivision(working_split)
            fused_splits[str(working_split)] = list(zip(splits_dict[str(each_split_name)],
                                                        splits_dict[str(working_split[0]+"y"+working_split[-1])]))


    #print(fused_splits)

    left_eye = fused_splits["lt"]+fused_splits["lb"]
    right_eye = fused_splits["rt"]+fused_splits["rb"]

    eyes = (left_eye, right_eye)

    #print("")
    face_image = Image.fromarray(input_image)


    #print("Loading eye graphic...")
    new_eye = Image.open(str("media/eye_input/frame" + str("%0*d" % (3, __framenr)) + ".png"), "r")

    #print("Fitting graphic to left eye...")
    # Setting up left eye imagery
    left_image_scale = (int(left_eye_width+(left_eye_width*pad_percent)),
                        int(left_eye_width+(left_eye_width*pad_percent)))

    # Making a blank image the same size as the face input image, and placing the new eye where the original eye is
    new_left_eye = Image.new("RGBA", face_image.size, (0, 0, 0, 0))
    new_left_eye.paste(new_eye.resize(left_image_scale, Image.LANCZOS),
                       (int(left_eye_true_center[0]-(left_image_scale[0]/2)),
                        int(left_eye_true_center[-1]-(left_image_scale[0]/2))))

    left_eye_mask = Image.new("L", new_left_eye.size, 0)

    # Drawing the mask of the left eye
    drw_left_eye_mask = ImageDraw.Draw(left_eye_mask, "L")
    drw_left_eye_mask.polygon(left_eye, fill=255)


    # Setting up right eye
    right_image_scale = (int(right_eye_width+(right_eye_width*pad_percent)),
                         int(right_eye_width+(right_eye_width*pad_percent)))

    # Making a blank image the same size as the face input image, and placing the new eye where the original eye is
    new_right_eye = Image.new("RGBA", face_image.size, (0, 0, 0, 0))
    new_right_eye.paste(new_eye.resize(right_image_scale, Image.LANCZOS),
                        (int(right_eye_true_center[0]-(right_image_scale[0]/2)),
                        int(right_eye_true_center[-1]-(right_image_scale[0]/2))))

    right_eye_mask = Image.new("L", new_right_eye.size, 0)

    # Drawing the mask of the right eye
    drw_right_eye_mask = ImageDraw.Draw(right_eye_mask, "L")
    drw_right_eye_mask.polygon(right_eye, fill=255)

    # Feathering masks
    left_eye_mask = left_eye_mask.filter(ImageFilter.GaussianBlur(mask_feather))
    right_eye_mask = right_eye_mask.filter(ImageFilter.GaussianBlur(mask_feather))

    #print("Rendering frame "+str(int(0))+"...")
    # Rendering the new eyes
    face_image.paste(new_left_eye, mask=left_eye_mask)
    face_image.paste(new_right_eye, mask=right_eye_mask)

    if __testing:
        face_image.show()
    else:
        face_image.save(str("media/face_output/"+str(__frame)), format="PNG")
