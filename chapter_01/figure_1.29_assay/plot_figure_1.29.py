#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-26
# file: plot_figure_1.29.py
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

def Plot(X, outname, outdir, pColors, labelString = None,
         titlestr = None, params = None, grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.direction'] = 'in'
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
        getFigureProps(width = 6.0, height = 4.0,
                       lFrac = 0.10, rFrac = 0.95,
                       bFrac = 0.15, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    ######################################################################################
    labelfontsize = 6.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 2.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$y - t$', fontsize = 7.0)
    ax1.set_ylabel(r'$|y-t|^{q}$', fontsize = 7.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0

    ######################################################################################
    # plotting

    lineWidth = 0.65

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 1,
             label = r'')

    ######################################################################################
    # annotations
    if labelString:
        ax1.annotate(labelString,
                     xy = (0.5, 0.7),
                     xycoords = 'axes fraction',
                     fontsize = 8.0,
                     horizontalalignment = 'center')

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
        xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor = xFormat
        major_x_ticks = np.arange(xTicksMin, xTicksMax, dxMajor)
        minor_x_ticks = np.arange(xTicksMin, xTicksMax, dxMinor)
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
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

    # figure 1.29 Bishop - Chapter 1 Introduction
    
    pColors = {'red': '#FF0000'} # standard red
    
    xFormat = (-2.0, 2.0, -2.0, 2.05, 1.0, 1.0)
    yFormat = (0.0, 2.0, 0.0, 2.05, 1.0, 1.0)

    ######################################################################################
    # A q = 0.3
    nVisPoints = 500
    xVals_leftBranch = np.linspace(-2.1, -0.002, nVisPoints)
    xVals_centerBranch = np.linspace(-0.002, 0.002, 2 * nVisPoints)
    xVals_rightBranch = np.linspace(0.002, 2.1, nVisPoints)
    xVals = np.concatenate((xVals_leftBranch, xVals_centerBranch, xVals_rightBranch), axis = 0)

    yVals = np.abs(xVals) ** 0.3
    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."

    X = np.zeros((len(xVals), 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # call the plotting function

    outname = 'prml_ch_01_figure_1.29_A'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = r'$q = 0.3$',
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)


    #######################################################################################
    # B q = 1
    nVisPoints = 500
    xVals = np.linspace(-2.1, 2.1, nVisPoints)
    yVals = np.abs(xVals)
    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."

    X = np.zeros((len(xVals), 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # call the plotting function

    outname = 'prml_ch_01_figure_1.29_B'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = r'$q = 1$',
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)

    #######################################################################################
    # C q = 2
    nVisPoints = 500
    xVals = np.linspace(-2.1, 2.1, nVisPoints)
    yVals = xVals ** 2
    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."

    X = np.zeros((len(xVals), 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # call the plotting function

    outname = 'prml_ch_01_figure_1.29_C'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = r'$q = 2$',
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)
                   

    #######################################################################################
    # D q = 10
    nVisPoints = 500
    xVals = np.linspace(-2.1, 2.1, nVisPoints)
    yVals = xVals ** 10
    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."

    X = np.zeros((len(xVals), 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # call the plotting function

    outname = 'prml_ch_01_figure_1.29_D'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = r'$q = 10$',
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)
