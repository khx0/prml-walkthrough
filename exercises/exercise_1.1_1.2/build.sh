#!/bin/bash
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# build local TeX document from source
# date: 2018-10-06
##########################################################################################

# tex sheet
pdflatex main.tex
bibtex main.aux
pdflatex main.tex
pdflatex main.tex
pdflatex main.tex

# clean up auxiliary files
rm *.aux *.log  *.out *.toc *.bbl *.blg *.xwm

