#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-192
# file: plot_figure_1.28.py
# tested with python 3.7.6 in conjunction with mpl version 3.1.3
##########################################################################################

import os
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

def Plot(titlestr, Xm, X, params, outname, outdir, pColors,
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc("axes", linewidth = 1.0)

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
        getFigureProps(width = 5.0, height = 4.0,
                       lFrac = 0.15, rFrac = 0.95,
                       bFrac = 0.09, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    # remove right and top axes
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    ######################################################################################
    labelfontsize = 8.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 0.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 0.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$x$', fontsize = 8.0, x = 0.95)
    # rotation (angle) is expressed in degrees
    ax1.set_ylabel(r'$t$', fontsize = 8.0, y = 0.85,
                   rotation = 0.0)
    ax1.xaxis.labelpad = -7.0
    ax1.yaxis.labelpad = -16.0
    ######################################################################################
    # plotting

    lineWidth = 1.0

    x0 = params[0]

    plt.axvline(x = x0,
                color = 'k',
                lw = lineWidth,
                zorder = 4)

    ax1.plot(Xm[:, 0], Xm[:, 1],
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 3,
             label = r'')

    ax1.plot([xFormat[0], x0], [0.0, 0.0],
             color = pColors['green'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'',
             dashes = [4.0, 2.0])

    ax1.plot(X[:, 1], X[:, 0],
             color = pColors['blue'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 5,
             label = r'')

    ######################################################################################
    # x axis arrow head
    ax1.arrow(xFormat[1], yFormat[0], 0.5, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = 0.6,
              head_length = 0.5,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    # y axis arrow head
    ax1.arrow(xFormat[0], yFormat[1], 0.0, 0.5,
              lw = 0.5,
              color = 'k',
              head_width = 0.5,
              head_length = 0.6,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    ######################################################################################
    # annotations

    label = r'$p(t\, | \, x_0)$'
    x_pos = 0.64
    ax1.annotate(label,
                 xy = (x_pos, 0.34),
                 xycoords = 'axes fraction',
                 fontsize = 8.0,
                 horizontalalignment = 'center')

    label = r'$y(x)$'
    x_pos = 0.80
    ax1.annotate(label,
                 xy = (x_pos, 0.83),
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
    # set plot range
    if xFormat == None:
        pass
    else:
        ax1.set_xlim(xFormat[0], xFormat[1])
        ax1.set_xticks([x0])
        ax1.set_xticklabels([r'$x_0$'])

    if yFormat == None:
        pass
    else:
        ax1.set_ylim(yFormat[0], yFormat[1])
        ax1.set_yticks([0.0])
        ax1.set_yticklabels([r'$y(x_0)$'])

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
    if savePDF: # use pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

def entropy(x):
    '''
    Computes the discrete entropy of the given
    probabilities x.
    '''
    H = 0.0
    for pi in x:
        if np.isclose(pi, 0.0):
            continue
        else:
            H += -pi * np.log(pi)
    return H

    # return -x.dot(np.log(x))

if __name__ == '__main__':

#     x = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
# 
#     # x = np.array([0.5, 0.5])
# 
#     print(np.sum(x))
#     
#     H = entropy(x)
#     
#     print("H =", H)
#     print(np.log(5))
    
    ##################################################

#     nBins = 30
#     x = np.zeros((nBins,))
#     print(x.shape)
# 
#     x[15] = 0.27
#     x[13] = x[16] = 0.23
#     x[12] = x[17] = 0.10
#     x[11] = x[18] = 0.03
#     x[10] = x[19] = 0.005
# 
#     print(np.sum(x))
#     print(entropy(x))
#     
    
    xmin, xmax = 0.0, 1.0
    nBins = 30
    dx = (xmax - xmin) / float(nBins)
    bins = np.linspace(xmin, xmax, nBins + 1)
    binCenters = bins[:-1] + dx / 2.0
    print("bins =", binCenters)
    print("bins.shape =", binCenters.shape)
    
    print(binCenters[14])
    print(binCenters[15])
    
    values = np.zeros((nBins,))
    
    selectorSet = [10, 11, 12, 13, 14, 15, 16, 17, 18]

    values[selectorSet] = norm.pdf(binCenters[selectorSet],
        loc = binCenters[14],
        scale = 0.048)
        
    normVal = np.sum(values)
    
    values /= normVal
    
    
    print(entropy(values))
    
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1)
    ax.scatter(binCenters, values,
               s = 10)
    # ax.legend(loc='best', frameon=False)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 0.5)
    plt.show()
    
    
    
    
    '''
    # figure 1.16 Bishop - Chapter 1 Introduction

    # plot color dictionary
    pColors = {'green': '#00FF00', # neon green
               'red':   '#FF0000', # standard red
               'blue':  '#0000FF'} # standard blue

    # query point (arbirtarily chosen here)
    x0 = 0.0

    # create the synthetic data for the polynomial (red) curve
    nVisPoints = 1000
    xVals = np.linspace(-10.0, 10.0, nVisPoints)
    yVals = np.array([0.005 * (x ** 3 + x ** 2 + 80.0 * x)  for x in xVals])
    Xm = np.zeros((nVisPoints, 2))
    Xm[:, 0] = xVals
    Xm[:, 1] = yVals

    # create normal distribution with specified mean and variance (location and shape)
    # pdf function signature
    # scipy.stats.norm(x, loc, scale)

    mu  = 0.0        # mean of the normal distribution $\mu$
    var = 1.5 ** 2   # variance of the normal distribution $\sigma^2§

    ######################################################################################
    # IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
    # not the variance as scale parameter. This is one of the most frequent pitfalls
    # when using normal distributions.
    ######################################################################################

    nVisPoints = 1000
    xVals = np.linspace(-12.0, 12.0, nVisPoints)
    yVals = 10.0 * np.array([norm.pdf(x, loc = mu, scale = np.sqrt(var)) for x in xVals])

    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # xLeft and xRight are the x coordinates $\mu - \sigma$ and $\mu + \sigma$.
    # Pay attention that we use the standard deviation $\sigma$ here and not the
    # variance $\sigma^2$.
    xLeft  = mu - np.sqrt(var)
    xRight = mu + np.sqrt(var)

    yLeft  = norm.pdf(xLeft, mu, np.sqrt(var))
    yRight = norm.pdf(xRight, mu, np.sqrt(var))

    assert np.isclose(yLeft, yRight), "Error: yLeft == yRight assertion failed."
    ######################################################################################
    # call the plotting function

    outname = 'prml_ch_01_figure_1.28'

    xFormat = [-11.1, 11.1]
    yFormat = [-10.5, 10.5]

    outname = Plot(titlestr = '',
                   Xm = Xm,
                   X = X,
                   params = [x0],
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)
    '''