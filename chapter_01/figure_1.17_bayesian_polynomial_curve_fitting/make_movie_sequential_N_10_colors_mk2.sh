#!/bin/bash
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# file: make_movie_sequential_N_10_colors_mk2.sh
# date: 2019-02-10
##########################################################################################

ffmpeg -framerate 2 -pattern_type glob -i './out/frames_sequential_N_10_colors_mk2/*.png' \
       -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p \
       ./out/BayesianPolyCurveFitting_M_9_N_10_colors_mk2.mp4
