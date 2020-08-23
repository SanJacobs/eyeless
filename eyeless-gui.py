#!/usr/bin/env python3

import GUI
import jobs

path = GUI.load_init_popup()

if path != "":
    print("Received path: " + path)
    GUI.load_main_window(path)
