#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-22
# file: plot_figure_1.2.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.3
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

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

def Plot(X, Xt, outname, outdir, pColors, titlestr = None,
         grid = False, drawLegend = False, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc('axes', linewidth = 0.5)

    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica'
    # the above two lines could also be replaced by the single line below
    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac = \
        getFigureProps(width = 4.1, height = 2.9,
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

    ax1.tick_params('both', length = 1.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(r'$x$', fontsize = 6.0, x = 0.85)
    # rotation (angle) is expressed in degrees
    ax1.set_ylabel(r'$t$', fontsize = 6.0, y = 0.70, rotation = 0.0)
    ax1.xaxis.labelpad = -1.75
    ax1.yaxis.labelpad = -1.75
    ######################################################################################
    # plotting

    lineWidth = 0.65

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors['green'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.scatter(Xt[:, 0], Xt[:, 1],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = pColors['blue'],
                zorder = 3,
                label = r'')

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
    # set plot range
    if xFormat == None:
        pass
    else:
        major_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[4])
        minor_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[5])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xFormat[0], xFormat[1])

    if yFormat == None:
        pass
    else:
        major_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[4])
        minor_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[5])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(yFormat[0], yFormat[1])

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
    if savePDF: # save to file using pdf backend
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

    # figure 1.2 - Bishop - Chapter 1 Introduction

    # create ground truth data
    n_vispoints = 800
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    yVals = np.sin(2.0 * np.pi * xVals)

    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # noise settings

    # fix random number seed for reproducibility
    seed_value = 523456789
    seed = np.random.seed(seed_value)

    # numpy.random.normal() function signature:
    # numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
    # loc = mean ($\mu$)
    # scale = standard deviation ($\sigma$)
    # $\mathcal{N}(\mu, \sigma^2)$
    mu = 0.0
    sigma = 0.3

    # create N training data points (N = 10)
    # Xtrain = training data set
    N = 10
    xtrainVals = np.linspace(0.0, 1.0, N)
    ytrainVals = np.sin(2.0 * np.pi * xtrainVals) + \
        np.random.normal(mu, sigma, xtrainVals.shape)
    Xtrain = np.zeros((N, 2))
    Xtrain[:, 0] = xtrainVals
    Xtrain[:, 1] = ytrainVals

    # call the plotting function
    outname = f'prml_ch_01_figure_1.2_PRNG_seed_{seed_value}'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xFormat = (-0.05, 1.05, 0.0, 1.1, 1.0, 1.0)
    yFormat = (-1.35, 1.35, -1.0, 1.1, 1.0, 1.0)

    # plot color dictionary
    pColors = {'blue':  '#0000FF',
               'green': '#00FF00'}

    outname = Plot(X = X,
                   Xt = Xtrain,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   xFormat = xFormat,
                   yFormat = yFormat)
