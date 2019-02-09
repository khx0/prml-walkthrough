#!/bin/bash
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# file: make_movie_sequential.sh
# date: 2019-02-09
##########################################################################################

ffmpeg -framerate 2 -pattern_type glob -i './out/frames_sequential/*.png' \
       -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p ./out/BayesianPolyCurveFitting_M_9.mp4
