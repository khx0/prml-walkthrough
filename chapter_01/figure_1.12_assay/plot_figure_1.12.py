#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-28
# file: plot_figure_1.12.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.1
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

from scipy.stats import norm

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def getFigureProps(width, height, lFrac = 0.17, rFrac = 0.9, bFrac = 0.17, tFrac = 0.9):
    '''
    True size scaling auxiliary function to setup mpl plots with a desired size.
    Specify widht and height in cm.
    lFrac = left fraction   in [0, 1]
    rFrac = right fraction  in [0, 1]
    bFrac = bottom fraction in [0, 1]
    tFrac = top fraction    in [0, 1]
    returns:
        fWidth = figure width
        fHeight = figure height
    These figure width and height values can then be used to create a figure instance
    of the desired size, such that the actual plotting canvas has the specified
    target width and height, as provided by the input parameters of this function.
    '''
    axesWidth = width / 2.54    # convert to inches
    axesHeight = height / 2.54  # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def Plot(X, outname, outdir, pColors, titlestr = None, params = None,
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'inout'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc('axes', linewidth = 0.5)

    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 4.4, height = 3.2,
                       lFrac = 0.10, rFrac = 0.95,
                       bFrac = 0.15, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    # minimal layout
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    ######################################################################################
    labelfontsize = 6.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 4.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$x$', fontsize = 6.0, x = 0.95)
    ax1.set_ylabel(r'', fontsize = 6.0)
    ax1.xaxis.labelpad = 1.0
    ax1.yaxis.labelpad = -18.0

    ######################################################################################
    # quiver arrows

    # x-axis arrow
#     x_pos = 0.96 * xFormat[1]
#     y_pos = yFormat[0]
#     x_direct = 1.0
#     y_direct = 0.0
# 
#     ax1.quiver(x_pos, y_pos, x_direct, y_direct,
#                units = 'dots',
#                scale = 15.0,
#                scale_units = 'height',
#                width = 0.5,
#                headwidth = 6.0,
#                headlength = 7.0,
#                headaxislength = 5.5,
#                clip_on = False,
#                zorder = 4)
# 
#     # y-axis arrow
#     x_pos = xFormat[0]
#     y_pos = 0.95 * yFormat[1]
#     x_direct = 0.0
#     y_direct = 1.0
# 
#     ax1.quiver(x_pos, y_pos, x_direct, y_direct,
#                units = 'dots',
#                scale = 15.0,
#                scale_units = 'height',
#                width = 0.5,
#                headwidth = 6.0,
#                headlength = 7.0,
#                headaxislength = 5.5,
#                clip_on = False,
#                zorder = 4)
# 
# 
#     Lx = np.abs(xFormat[1] - xFormat[0])
#     dx = 0.97 * np.sqrt(var)

#     x_pos = mu
#     y_pos = yLeft
#     x_direct = 1.0
#     y_direct = 0.0
# 
#     ax1.quiver(x_pos, y_pos, x_direct, y_direct,
#                units = 'dots',
#                scale = Lx / dx,
#                scale_units = 'width',
#                width = 0.5,
#                headwidth = 6.0,
#                headlength = 7.0,
#                headaxislength = 5.5,
#                clip_on = False,
#                zorder = 4)


#     x_pos = mu
#     y_pos = yLeft
#     x_direct = -1.0
#     y_direct = 0.0
# 
#     ax1.quiver(x_pos, y_pos, x_direct, y_direct,
#                units = 'dots',
#                scale = Lx / dx,
#                scale_units = 'width',
#                width = 0.5,
#                headwidth = 6.0,
#                headlength = 7.0,
#                headaxislength = 5.5,
#                clip_on = False,
#                zorder = 4)

    ######################################################################################
    # plotting

    lineWidth = 0.65

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ######################################################################################
    # annotations

#     label = r'$2\sigma$'
# 
#     x_pos = 0.5
# 
#     ax1.annotate(label,
#                  xy = (x_pos, 0.47),
#                  xycoords = 'axes fraction',
#                  fontsize = 6.0,
#                  horizontalalignment = 'center')

    ######################################################################################
    # legend
    if drawLegend:
        leg = ax1.legend(# bbox_to_anchor = [0.7, 0.8],
                         # loc = 'upper left',
                         handlelength = 1.5,
                         scatterpoints = 1,
                         markerscale = 1.0,
                         ncol = 1)
        leg.draw_frame(False)
        plt.gca().add_artist(leg)

    ######################################################################################
    # set plot range and scale
    if xFormat == None:
        pass # mpl autoscale
    else:
        xmin, xmax = xFormat
        ax1.set_xticks([])
        ax1.set_xlim(xmin, xmax) # set x limits last (order matters here)
    if yFormat == None:
        pass # mpl autoscale
    else:
        ymin, ymax = yFormat
        ax1.set_yticks([])
        ax1.set_ylim(ymin, ymax) # set y limits last (order matters here)

    ######################################################################################
    # set plot range
#     if xFormat == None:
#         pass
#     else:
#         ax1.set_xlim(xFormat[0], xFormat[1])
#         # ax1.set_xticks([params[0]])
#         ax1.set_xticklabels([r'$\mu$'])
# 
#     if yFormat == None:
#         pass
#     else:
#         ax1.set_ylim(yFormat[0], yFormat[1])
#         ax1.set_yticklabels([])
#         ax1.set_yticks([])

    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)

    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.2)
        ax1.grid(True)
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.1)
        ax1.grid(True, which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF:
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    # figure 1.12 Bishop - Chapter 1 Introduction

    nVisPoints = 800
    xVals = np.linspace(0.0, 1.0, nVisPoints)

    yVals_01 = 1.22 * norm.pdf(xVals,
                               loc = 0.28, 
                               scale = np.sqrt(0.015))

    yVals_02 = 1.5 * norm.pdf(xVals,
                              loc = 0.62,
                              scale = np.sqrt(0.007))

    yVals = yVals_01 +  yVals_02

    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # call the plotting function

    outname = 'prml_ch_01_figure_1.12'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xFormat = (0.0, 1.0)
    yFormat = (0.0, 8.0)

    pColors = {'red': '#FF0000'} # standard red

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)
