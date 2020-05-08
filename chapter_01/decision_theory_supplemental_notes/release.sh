#!/bin/bash
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# file: release.sh
# date: 2020-05-08
# build and release local TeX document with timestamp
##########################################################################################

# run pdflatex on the main.tex file
pdflatex main.tex
bibtex main.aux
pdflatex main.tex
pdflatex main.tex
pdflatex main.tex

# clean up auxiliary files
rm *.aux *.log  *.out *.toc *.bbl *.blg *.xwm

outname="Supplemental_Notes_on_Decision_Theory_$(date +%Y-%m-%d).pdf"

echo $outname

mv main.pdf $outname