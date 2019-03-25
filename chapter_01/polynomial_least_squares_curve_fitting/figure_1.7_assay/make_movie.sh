#!/bin/bash
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# file: make_movie.sh
# date: 2019-03-25
##########################################################################################

ffmpeg -framerate 16 -pattern_type glob -i './frames/*.png' \
       -r 30 -f mp4 -vcodec libx264 -pix_fmt yuv420p \
       ./out/figure_1.7_regularization_variation.mp4
