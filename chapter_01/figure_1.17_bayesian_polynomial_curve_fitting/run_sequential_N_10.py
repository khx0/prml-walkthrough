#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-09-05
# file: run_sequential_N_10.py
# tested with python 3.7.2  using matplotlib 3.1.1
##########################################################################################

import os
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

from bayesianPolyCurveFit import bayesianPolyCurveFit

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out/frames_sequential_N_10')

os.makedirs(RAWDIR, exist_ok = True)
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

def Plot(titlestr, X_gt, Xt, Xm, params, outname, outdir, pColors,
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 5.0})
    mpl.rc("axes", linewidth = 0.5)

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
        getFigureProps(width = 3.6, height = 2.42,
                       lFrac = 0.10, rFrac = 0.95,
                       bFrac = 0.32, tFrac = 0.92)
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
    plt.title(titlestr)
    ax1.set_xlabel(r'$x$', fontsize = 6.0, x = 0.85)
    # rotation (angle) is expressed in degrees
    ax1.set_ylabel(r'$t$', fontsize = 6.0, y = 0.70, rotation = 0.0)
    ax1.xaxis.labelpad = -1.75
    ax1.yaxis.labelpad = -0.5
    ######################################################################################
    # plotting

    lineWidth = 0.65

    p1, = ax1.plot(X_gt[:, 0], X_gt[:, 1],
                  color = pColors['green'],
                  alpha = 1.0,
                  lw = lineWidth,
                  zorder = 2,
                  label = r'ground truth')

    nDatapoints = len(Xt)
    labelString = r'observed data ($N = %d$)' %(nDatapoints)

    p2 = ax1.scatter(Xt[:, 0], Xt[:, 1],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = pColors['blue'],
                zorder = 3,
                label = labelString)

    p3, = ax1.plot(Xm[:, 0], Xm[:, 1],
                  color = pColors['red'],
                  alpha = 1.0,
                  lw = lineWidth,
                  zorder = 2,
                  label = r'predicted mean $\mu(x)$')

    error = np.sqrt(Xm[:, 2]) # use standard deviation
    p4 = ax1.fill_between(Xm[:, 0], Xm[:, 1] - error, Xm[:, 1] + error,
                          color = pColors['red'],
                          alpha = 0.20,
                          lw = 0.0,
                          zorder = 2,
                          label = r'model uncertainty $\mu(x) \pm \sigma(x)$')

    ######################################################################################
    # annotations

    label = r'polynomial degree $M = 9$'

    ax1.annotate(label,
                 xy = (1.0, 1.03),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'right')

    ######################################################################################
    # legend
    if drawLegend:

        pHandles = [p1, p2, p3, p4]
        pLabels = [handle.get_label() for handle in pHandles]

        leg = ax1.legend(pHandles,
                         pLabels,
                         bbox_to_anchor = [0.07, 0.02],
                         loc = 'upper left',
                         handlelength = 1.5,
                         scatterpoints = 1,
                         markerscale = 1.0,
                         ncol = 1)
        leg.draw_frame(False)
        plt.gca().add_artist(leg)

    # legend([ht,h1.patches[0],hb],[H.get_label() for H in hh])

    ######################################################################################
    # set plot range
    if (xFormat == None):
        pass
    else:
        major_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[4])
        minor_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[5])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xFormat[0], xFormat[1])

    if (yFormat == None):
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

    # create ground truth data
    nVisPoints = 1000
    xVals = np.linspace(-0.25, 1.25, nVisPoints)
    yVals = np.sin(2.0 * np.pi * xVals)
    X_gt = np.zeros((nVisPoints, 2))
    X_gt[:, 0] = xVals
    X_gt[:, 1] = yVals

    # input file i/o (load training data)
    seedValue = 523456789
    filename = 'prml_ch_01_figure_1.2_training_Data_PRNG-seed_{}.txt'.format(seedValue)

    data = np.genfromtxt(os.path.join(RAWDIR, filename))
    assert data.shape[1] == 2, "Error: Shape assertion failed."
    print("data.shape =", data.shape)
    nDatapoints = data.shape[0]

    X, T = data[:, 0], data[:, 1] # using the Bishop naming convention

    # set (hyper-) parameters for the Bayesian polynomial curve fitting
    alpha = 5.0e-3
    beta = 11.1
    M = 9 # order of polynomial
    xSupport = np.linspace(-0.25, 1.25, 500)

    xFormat = [-0.035, 1.035, 0.0, 1.1, 1.0, 1.0]
    yFormat = [-1.55, 1.55, -1.0, 1.1, 1.0, 1.0]

    # plot color dictionary
    pColors = {'green': '#00FF00', # neon green
               'red':   '#FF0000', # standard red
               'blue':  '#0000FF'} # standard blue

    # fix random seed for reproducibility
    np.random.seed(823456789)
    idxs = np.random.permutation(nDatapoints)

    for i in range(nDatapoints):

        # incremental build up by using the subset of indices as specified in selector
        selector = idxs[0:i + 1]
        print(i, selector)

        res = bayesianPolyCurveFit(xSupport, X[selector], T[selector], alpha, beta, M)

        outname = 'sequential_training_seed_523456789_frame_' + str(i).zfill(2)

        outname = Plot(titlestr = '',
                       X_gt = X_gt,
                       Xt = data[selector],
                       Xm = res,
                       params = [],
                       outname = outname,
                       outdir = OUTDIR,
                       pColors = pColors,
                       grid = False,
                       drawLegend = True,
                       xFormat = xFormat,
                       yFormat = yFormat,
                       savePDF = False,
                       savePNG = True,
                       datestamp = False)
