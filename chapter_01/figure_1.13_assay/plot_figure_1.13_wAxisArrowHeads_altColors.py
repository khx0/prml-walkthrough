#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-04-20
# file: plot_figure_1.13_wAxisArrowHeads_altColors.py
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

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

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

def Plot(titlestr, X, params, outname, outdir, pColors,
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'inout'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
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
        getFigureProps(width = 4.4, height = 3.2,
                       lFrac = 0.10, rFrac = 0.95, bFrac = 0.15, tFrac = 0.95)
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
    ax1.set_xlabel(r'$x$', fontsize = 6.0, x = 0.98)
    # rotation (angle) is expressed in degrees
    ax1.set_ylabel(r'$\mathcal{N}(x\, | \, \mu, \sigma^2)$', fontsize = 6.0, y = 0.85,
                   rotation = 0.0)
    ax1.xaxis.labelpad = -6.5
    ax1.yaxis.labelpad = -18.0
    ######################################################################################
    # plotting

    lineWidth = 0.65

    Lx = xFormat[1] - xFormat[0]
    Ly = yFormat[1] - yFormat[0]
    XoverY = Lx / Ly

    # x axis arrow head
    dx = 0.02 # x displacement of the arrow head
    hWidth = 0.0115
    hLength = 0.1
    ax1.arrow(7.0, 0.0, dx, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    # y axis arrow head
    dy = dx / XoverY
    ax1.arrow(0.0, 0.55, 0.0, dy,
              lw = 0.5,
              color = 'k',
              head_width = hLength,
              head_length = hWidth,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.arrow(mu, yLeft, - 0.94 * np.sqrt(var), 0.0,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = True)

    ax1.arrow(mu, yRight, 0.94 * np.sqrt(var), 0.0,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = True)

    ######################################################################################
    # annotations

    label = r'$2\sigma$'

    x_pos = 0.5

    ax1.annotate(label,
                 xy = (x_pos, 0.47),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
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
    # set plot range
    if (xFormat == None):
        pass
    else:
        ax1.set_xlim(xFormat[0], xFormat[1])
        ax1.set_xticks([params[0]])
        ax1.set_xticklabels([r'$\mu$'])

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
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.2)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.1)
        ax1.grid('on', which = 'minor')
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

    # figure 1.13 Bishop - Chapter 1 Introduction

    ######################################################################################
    # create normal distribution with specified mean and variance (location and shape)
    # pdf function signature
    # scipy.stats.norm(x, loc, scale)

    ######################################################################################
    # IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
    # not the variance as scale parameter. This is one of the most frequent pitfalls
    # when using normal distributions.
    ######################################################################################

    mu = 3.5    # mean of the normal distribution $\mu$
    var = 1.0   # variance of the normal distribution $\sigma^2$

    nVisPoints = 800
    xVals = np.linspace(0.0, 20.0, nVisPoints)
    yVals = norm.pdf(xVals, loc = mu, scale = np.sqrt(var))

    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # xLeft and xRight are the x coordinates $\mu - \sigma$ and $\mu + \sigma$.
    # Pay attention that we use the standard deviation $\sigma$ here and not the
    # variance $\sigma^2$.

    xLeft = mu - np.sqrt(var)
    xRight = mu + np.sqrt(var)

    yLeft = norm.pdf(xLeft, mu, np.sqrt(var))
    yRight = norm.pdf(xRight, mu, np.sqrt(var))

    assert np.isclose(yLeft, yRight), "Error: yLeft == yRight assertion failed."

    ######################################################################################
    # call the plotting function

    xFormat = [0.0, 7.0]
    yFormat = [0.0, 0.55]

    outnames = ['prml_ch_01_figure_1.13_wAxisArrowHeads_altColors_k',
                'prml_ch_01_figure_1.13_wAxisArrowHeads_altColors_C0',
                'prml_ch_01_figure_1.13_wAxisArrowHeads_altColors_C3']

    pColorsArray = [['k'],
                    ['C0'],
                    ['C3']]

    for pColors, outname in zip(pColorsArray, outnames):

        outname = Plot(titlestr = '',
                       X = X,
                       params = [mu, var],
                       outname = outname,
                       outdir = OUTDIR,
                       pColors = pColors,
                       grid = False,
                       drawLegend = False,
                       xFormat = xFormat,
                       yFormat = yFormat)
