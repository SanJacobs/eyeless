# Eyeless
A tool that tracks people's eyes to replace them with any image or image sequence.
The GUI version is currently under development, but the command-line prototype is functional.

## Usage

### 0. Find a video

For the best results, avoid videos where:
 - Hair covers the face
 - Subject is wearing glasses
 - Head is tilted more than 45 degrees to either side
 - Everything is really dark


### 1. Prepare the video

Render out all frames of video as PNGs named exactly as such:
 - frame00001.png
 - frame00002.png
 - frame00003.png
 - (...)
 - frame00475.png

Start counting from 1, not 0.
These can be any resolution you want.


### 2. Prepare the eyes

Again, PNGs, named as such:
 - frame001.png
 - frame002.png
 - frame003.png
 - (...)
 - frame078.png

Make sure the last and first frames of the animation are not duplicates,
otherwise there will be an awkward stutter with every loop.

A good animation contains:
 - Darkened corners
 - Reflected lights in eyes
 - Simple readable shape


# # TODO Write the rest of the README.
