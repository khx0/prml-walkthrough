#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-29
# file: plot_figure_1.23_custom.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.3
##########################################################################################

import os
import platform
import datetime
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from unitSphereArea import p_of_r_GaussianDistribution

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def cleanFormatter(x, pos):
    '''
    will format 0.0 as 0 and
    will format 1.0 as 1
    '''
    return '{:g}'.format(x)

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
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 4.0, height = 3.0,
                       lFrac = 0.15, rFrac = 0.96,
                       bFrac = 0.17, tFrac = 0.95)
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

    ax1.tick_params('both', length = 2.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(r'$r$', fontsize = 6.0)
    ax1.set_ylabel(r'$p(r)$', fontsize = 6.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################
    # plotting

    lineWidth = 0.65

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors['blue'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             clip_on = True)

    ax1.plot(X[:, 0], X[:, 2],
             color = pColors['blue'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             clip_on = True)

    ax1.plot(X[:, 0], X[:, 3],
             color = pColors['blue'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             clip_on = True)

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

    ax1.annotate(r'$D = 1$',
                 xy = (0.05, 0.76),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 color = pColors['blue'],
                 horizontalalignment = 'left')

    ax1.annotate(r'$D = 2$',
                 xy = (0.18, 0.54),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 color = pColors['blue'],
                 horizontalalignment = 'left')

    ax1.annotate(r'$D = 20$',
                 xy = (0.61, 0.44),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 color = pColors['blue'],
                 horizontalalignment = 'left')

    ######################################################################################
    # set plot range

    if xFormat:
        major_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[4])
        minor_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[5])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xFormat[0], xFormat[1])
    if yFormat:
        major_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[4])
        minor_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[5])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(yFormat[0], yFormat[1])

    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

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

    # PRML Bishop Chapter 1 Introduction - Figure 1.23

    ######################################################################################
    # In the book the author does not state what value for $\sigma$ is used. I tried
    # $\sigma = 0.5$ which seems to reproduce the figure in the book quite well. Maybe
    # this educated guess is what was actually used in the book as well.
    sigma = 0.5
    ######################################################################################

    # create data
    n_vispoints = 1000
    X = np.zeros((n_vispoints, 4))
    xVals = np.linspace(0.0, 4.0, n_vispoints)
    X[:, 0] = xVals
    X[:, 1] = np.array([p_of_r_GaussianDistribution(r, sigma, 1) for r in xVals])
    X[:, 2] = np.array([p_of_r_GaussianDistribution(r, sigma, 2) for r in xVals])
    X[:, 3] = np.array([p_of_r_GaussianDistribution(r, sigma, 20) for r in xVals])

    # call the plotting function
    outname = 'prml_ch_01_figure_1.23_custom_#0000FF'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xFormat = (0.0, 4.1, 0.0, 4.05, 2.0, 1.0)
    yFormat = (0.0, 2.05, 0.0, 2.05, 1.0, 0.5)

    # plot color dictionary
    pColors = {'blue':  '#0000FF'}

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   xFormat = xFormat,
                   yFormat = yFormat)

    # call the plotting function
    outname = 'prml_ch_01_figure_1.23_custom_C0'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # plot color dictionary
    pColors = {'blue':  'C0'}

    outname = Plot(X = X,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   xFormat = xFormat,
                   yFormat = yFormat)
