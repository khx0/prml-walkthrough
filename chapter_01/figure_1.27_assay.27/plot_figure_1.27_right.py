#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-05-04
# file: plot_figure_1.27_right.py
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

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
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

def Plot(X, outname, outdir, pColors, titlestr = None,
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 6.0})
    mpl.rc("axes", linewidth = 0.5)

    # plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    plt.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 3.8, height = 3.0,
                       lFrac = 0.07, rFrac = 0.95,
                       bFrac = 0.11, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    # remove right and top axes
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ######################################################################################

    labelfontsize = 6.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 0.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.2)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.2, zorder = 10)
    ######################################################################################
    # labeling
    if titlestr: plt.title(titlestr)
    ax1.set_xlabel(r'', fontsize = 6.0)
    ax1.set_ylabel(r'', fontsize = 6.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################
    # plotting

    lineWidth = 0.65

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors['blue'],
             alpha = 1.0,
             lw = lineWidth,
             label = r'',
             clip_on = True,
             zorder = 1)

    ax1.plot(X[:, 0], X[:, 2],
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'',
             clip_on = True)

    ######################################################################################

    ax1.axhline(y = thetaVal, xmin = 0.0, xmax = xFormat[1],
                color = pColors['green'],
                lw = 0.5,
                dashes = [5.0, 3.0])

    ax1.axvline(x = xPos_1, 
                ymin = 0.0, 
                ymax = thetaVal / yFormat[1],
                color = pColors['green'],
                lw = 0.5)

    ax1.axvline(x = xPos_2, 
                ymin = 0.0, 
                ymax = thetaVal / yFormat[1],
                color = pColors['green'],
                lw = 0.5)

    # x axis arrow head (using arrow)
#     ax1.arrow(xFormat[1], 0.0, 0.05, 0.0,
#               lw = 0.5,
#               color = 'k',
#               head_width = 0.022,
#               head_length = 0.15,
#               length_includes_head = True,
#               clip_on = False,
#               zorder = 3)

    # y axis arrow head
#     ax1.arrow(xFormat[0], yFormat[1], 0.0, 0.015,
#               lw = 0.5,
#               color = 'k',
#               head_width = 0.11,
#               head_length = 0.028,
#               length_includes_head = True,
#               clip_on = False,
#               zorder = 3)

    # x axis arrow head (using quiver)
    x_pos = xFormat[1] - 0.16
    y_pos = 0.0
    x_direct = 1.0
    y_direct = 0.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct,
               units = 'dots',
               scale = 20.0,
               scale_units = 'height',
               width = 0.5,
               headwidth = 5.4,
               headlength = 6.0,
               headaxislength = 4.65,
               clip_on = False,
               zorder = 3)

    # y axis arrow head (using quiver)
    x_pos = xFormat[0]
    y_pos = yFormat[1] - 0.03
    x_direct = 0.0
    y_direct = 1.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct,
               units = 'dots',
               scale = 20.0,
               scale_units = 'height',
               width = 0.5,
               headwidth = 5.4,
               headlength = 6.0,
               headaxislength = 4.65,
               clip_on = False,
               zorder = 3)

    x_pos = xPos_1 + 1.0
    y_pos = -0.036
    x_direct = -3.35
    y_direct = 0.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct,
               units = 'dots',
               scale = 20.0,
               scale_units = 'height',
               width = 0.5,
               headwidth = 5.4,
               headlength = 6.0,
               headaxislength = 4.65,
               clip_on = False,
               zorder = 3)

    x_pos = xPos_1 + 1.0
    y_pos = -0.036
    x_direct = 5.5
    y_direct = 0.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct,
               units = 'dots',
               scale = 20.0,
               scale_units = 'height',
               width = 0.5,
               headwidth = 5.4,
               headlength = 6.0,
               headaxislength = 4.65,
               clip_on = False,
               zorder = 3)

#     yLevel = -0.04
#     ax1.arrow(xPos_1 + 1.0, yLevel, -1.0 + 0.05, 0.0,
#               lw = 0.5,
#               color = 'k',
#               head_width = 0.022,
#               head_length = 0.15,
#               length_includes_head = True,
#               clip_on = False)
# 
#     ax1.arrow(xPos_1 + 1.0, yLevel, xPos_2 - xPos_1 - 1.0 - 0.05, 0.0,
#               lw = 0.5,
#               color = 'k',
#               head_width = 0.022,
#               head_length = 0.15,
#               length_includes_head = True,
#               clip_on = False)

    ######################################################################################
    # legend
    #     if drawLegend:
    #         leg = ax1.legend(# bbox_to_anchor = [0.7, 0.8],
    #                          # loc = 'upper left',
    #                          handlelength = 1.5,
    #                          scatterpoints = 1,
    #                          markerscale = 1.0,
    #                          ncol = 1)
    #         leg.draw_frame(False)
    #         plt.gca().add_artist(leg)
    ######################################################################################
    # annotations

    ax1.annotate(r'$x$',
                 xy = (1.0, -0.06),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'$\theta$',
                 xy = (-0.032, 0.815),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'center',
                 verticalalignment = 'center')

    yLevel = 0.945

    ax1.annotate(r'$p(C_1|x)$',
                 xy = (0.155, yLevel),
                 xycoords = 'axes fraction',
                 fontsize = 5.5,
                 horizontalalignment = 'center')

    ax1.annotate(r'$p(C_2|x)$',
                 xy = (0.92, yLevel),
                 xycoords = 'axes fraction',
                 fontsize = 5.5,
                 horizontalalignment = 'center')

    ax1.annotate(r'reject region',
                 xy = (0.52, -0.105),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'center')

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
        ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor = yFormat
        major_y_ticks = np.arange(yTicksMin, yTicksMax, dyMajor)
        minor_y_ticks = np.arange(yTicksMin, yTicksMax, dyMinor)
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(ymin, ymax) # set y limits last (order matters here)

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

    # PRML Bishop Chapter 1 Introduction - Figure 1.27 (right)

    # load data
    filename = r'prml_ch_01_figure_1.26_p_of_C_k_given_x_data.npy'
    X = np.load(os.path.join(RAWDIR, filename))

    thetaVal = 0.9

    idx = np.argmin(np.abs(X[:, 1] - thetaVal))
    xPos_1 = X[:, 0][idx]
    idx = np.argmin(np.abs(X[:, 2] - thetaVal))
    xPos_2 = X[:, 0][idx]

    # call the plotting function
    outname = 'prml_ch_01_figure_1.26'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xFormat = (-0.5, 7.0)
    yFormat = (0.0, 1.085, 0.0, 1.05, 1.0, 1.0)

    # plot color dictionary
    pColors = {'blue':  '#0000FF',
               'green': '#00FF00',
               'red':   '#FF0000'}

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   xFormat = xFormat,
                   yFormat = yFormat)
