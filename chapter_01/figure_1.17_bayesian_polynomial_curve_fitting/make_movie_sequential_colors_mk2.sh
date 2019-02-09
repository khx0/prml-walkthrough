#!/bin/bash
##########################################################################################
# make_movie shell script
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# file: make_movie_sequential_colors_mk2.sh
# date: 2019-02-09
##########################################################################################

#ffmpeg -framerate 8 -i ./frames/frame_wHist_%03d.png -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p -vb 20M striped_major.mp4

# -vb 20M

ffmpeg -framerate 2 -pattern_type glob -i './out/frames_sequential_colors_mk2/*.png' \
    -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p BayesianPolyCurveFitting_M_9.mp4
