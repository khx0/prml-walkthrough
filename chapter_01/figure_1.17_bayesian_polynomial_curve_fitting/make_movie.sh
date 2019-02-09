#!/bin/bash
##########################################################################################
# make_movie shell script
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# file: make_movie.sh
# date: 2019-02-09
##########################################################################################

#ffmpeg -framerate 8 -i ./frames/frame_wHist_%03d.png -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p -vb 20M striped_major.mp4
ffmpeg -framerate 2 -pattern_type glob -i './out/increment_N/*.png' -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p test.mp4

# -vb 20M