#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-24
# file: plot_figure_1.24.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.3
##########################################################################################

import os
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

from scipy.stats import norm

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

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

def Plot(titlestr, X, outname, outdir, pColors,
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
        getFigureProps(width = 5.0, height = 3.0,
                       lFrac = 0.04, rFrac = 0.94, bFrac = 0.12, tFrac = 0.95)
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

    ax1.tick_params('both', length = 1.25, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.5)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.5, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'', fontsize = 6.0)
    ax1.set_ylabel(r'', fontsize = 6.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################
    # plotting

    lineWidth = 0.65

    ax1.plot(X[:, 0], X[:, 1],
             color = 'k',
             alpha = 1.0,
             lw = lineWidth,
                 zorder = 2,
                 label = r'',
                 clip_on = True)

    ax1.plot(X[:, 0], X[:, 2],
             color = 'k',
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'',
             clip_on = True)

    ######################################################################################
    # fill area under curve section

    idxs = X[:, 0] < x0_pos
    xPart = X[:, 0][idxs]
    yPart = X[:, 2][idxs]

    ax1.fill_between(xPart, yPart, y2 = 0.0,
                     color = pColors['green'],
                     alpha = fillAlphaValue,
                     lw = 0.0)

    idxs = np.logical_and(X[:, 0] < xHat_pos, X[:, 0] > x0_pos)
    xPart = X[:, 0][idxs]
    yPart1 = X[:, 1][idxs]
    yPart2 = X[:, 2][idxs]

    ax1.fill_between(xPart, yPart2, yPart1,
                     color = pColors['red'],
                     alpha = fillAlphaValue,
                     lw = 0.0)

    ax1.fill_between(xPart, yPart1, y2 = 0.0,
                     color = pColors['green'],
                     alpha = fillAlphaValue,
                     lw = 0.0)

    indices = X[:, 0] > xHat_pos
    xPart = X[:, 0][indices]
    yPart = X[:, 1][indices]

    ax1.fill_between(xPart, yPart, y2 = 0.0,
                     color = pColors['blue'],
                     alpha = fillAlphaValue,
                     lw = 0.0)

    ######################################################################################

    ax1.axvline(x = x0_pos, ymin = 0.0, ymax = 0.925,
                color = 'k',
                lw = 0.5,
                dashes = [5.0, 3.0])

    ax1.axvline(x = xHat_pos, ymin = 0.0, ymax = 0.925,
                color = 'k',
                lw = 0.5)

    # x axis arrow head
    ax1.arrow(xFormat[1], 0.0, 0.05, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = 0.012,
              head_length = 0.06,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    # y axis arrow head
    ax1.arrow(0.0, yFormat[1], 0.0, 0.015,
              lw = 0.5,
              color = 'k',
              head_width = 0.06,
              head_length = 0.012,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    yLevel = -0.023

    ax1.arrow(loc1, yLevel, -loc1 + 0.022, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = 0.012,
              head_length = 0.06,
              length_includes_head = True,
              clip_on = False)

    ax1.arrow(loc1, yLevel, 1.8 -0.022, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = 0.012,
              head_length = 0.06,
              length_includes_head = True,
              clip_on = False)

    ax1.arrow(loc2 + 0.5, yLevel, -0.5 + 0.022, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = 0.012,
              head_length = 0.06,
              length_includes_head = True,
              clip_on = False)

    ax1.arrow(loc2 + 0.5, yLevel, 1.75, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = 0.012,
              head_length = 0.06,
              length_includes_head = True,
              clip_on = False)

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
    # annotations

    ax1.annotate(r'$x$',
                 xy = (1.028, -0.02),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'$x_0$',
                 xy = (0.445, 0.94),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'center')

    ax1.annotate(r'$\hat{x}$',
                 xy = (0.602, 0.94),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'center')

    ax1.annotate(r'$p(x,\mathcal{C}_1)$',
                 xy = (0.12, 0.78),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'$p(x,\mathcal{C}_2)$',
                 xy = (0.67, 0.62),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'$\mathcal{R}_1$',
                 xy = (0.28, -0.105),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'$\mathcal{R}_2$',
                 xy = (0.80, -0.105),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

    ######################################################################################
    # set plot range

    if (xFormat == None):
        pass
    else:
        ax1.set_xlim(xFormat[0], xFormat[1])
        ax1.set_xticks([])
        ax1.set_xticklabels([])
    if (yFormat == None):
        pass
    else:
        ax1.set_ylim(yFormat[0], yFormat[1])
        ax1.set_yticklabels([])
        ax1.set_yticks([])

    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)

    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major', linewidth = 0.2)
        ax1.grid(True)
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor', linewidth = 0.1)
        ax1.grid(True, which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + now
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

    # PRML Bishop Chapter 1 Introduction - Figure 1.24

    # create data
    nVisPoints = 1500
    X = np.zeros((nVisPoints, 3))
    xVals = np.linspace(0.0, 5.5, nVisPoints)
    X[:, 0] = xVals

    ######################################################################################
    # IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
    # not the variance as scale parameter. This is one of the most frequent pitfalls
    # when using normal distributions.
    ######################################################################################

    # location (mean) of the normal distributions used in this example
    loc1 = 1.5
    loc2 = 3.3
    xHat_pos = loc2
    x0_pos = 2.4

    yVals = 0.59 * norm.pdf(xVals, loc = loc1, scale = np.sqrt(0.22))
    yVals += 0.31 * norm.pdf(xVals, loc = loc2, scale = np.sqrt(0.25))
    X[:, 1] = yVals

    yVals = 0.62 * norm.pdf(xVals, loc = loc2, scale = np.sqrt(0.34))
    X[:, 2] = yVals

    # call the plotting function
    outname = 'prml_ch_01_figure_1.24'

    xFormat = [0.0, 5.5, 0.0, 5.5, 1.0, 1.0]
    yFormat = [0.0, 0.62, 0.0, 0.62, 1.0, 1.0]

    fillAlphaValue = 0.5

    # plot color dictionary
    pColors = {'blue':  '#0000FF',
               'green': '#00FF00',
               'red':   '#FF0000'}

    outname = Plot(titlestr = '',
                   X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   grid = False,
                   drawLegend = True,
                   xFormat = xFormat,
                   yFormat = yFormat)
