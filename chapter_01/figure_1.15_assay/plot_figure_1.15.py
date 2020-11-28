#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-28
# file: plot_figure_1.15.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.3
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

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

def Plot(X, Xs, X_inferred, outname, outdir, pColors, titlestr = None,
         grid = False, drawLegend = False, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc('axes', linewidth = 1.0)

    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.0, height = 2.0,
                       lFrac = 0.05, rFrac = 0.95,
                       bFrac = 0.07, tFrac = 0.98)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    # minimal layout
    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    ######################################################################################
    labelfontsize = 6.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 3.5, width = 1.0, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(r'', fontsize = 8.0)
    ax1.set_ylabel(r'', fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0
    ######################################################################################
    # plotting

    lineWidth = 1.0

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors['green'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.plot(X_inferred[:, 0], X_inferred[:, 1],
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.scatter(Xs[:, 0], Xs[:, 1],
                s = 13.0,
                lw = lineWidth,
                facecolor = pColors['blue'],
                edgecolor = 'None',
                zorder = 11,
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
    # set plot range
    if xFormat:
        ax1.set_xlim(xFormat[0], xFormat[1])
        ax1.set_xticks([0])
        ax1.set_xticklabels([])

    if yFormat:
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

def mean_ML_estimator(X):
    '''
    i.e. the sample mean
    (assuming that X is a one dimensional data array)
    '''
    return np.sum(X) / float(len(X))

def variance_ML_estimator(X):
    '''
    i.e. the sample variance
    (assuming that X is a one dimensional data array)
    '''
    muML = mean_ML_estimator(X)
    return np.sum(np.square(X - muML)) / float(len(X))

if __name__ == '__main__':

    # figure 1.15 Bishop - Chapter 1 Introduction

    # plot color dictionary
    pColors = {'blue': '#0000FF',
               'green': '#00FF00',
               'red': '#FF0000'}

    ######################################################################################
    # create normal distribution with specified mean and variance (location and shape)
    # pdf function signature
    # scipy.stats.norm(x, loc, scale)

    ######################################################################################
    # IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
    # not the variance as scale parameter. This is one of the most frequent pitfalls
    # when using normal distributions.
    ######################################################################################

    mu    = 0.0  # mean of the normal distribution $\mu$
    var   = 1.4  # variance of the normal distribution $\sigma^2$
    sigma = np.sqrt(var)

    n_vispoints = 800
    xVals = np.linspace(-10.0, 10.0, n_vispoints)
    yVals = norm.pdf(xVals, loc = mu, scale = sigma)

    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    filenames = ['prml_ch_01_figure_1.15_A',
                 'prml_ch_01_figure_1.15_B',
                 'prml_ch_01_figure_1.15_C']

    samples = [[-1.7, -0.8],
               [-0.45, 0.45],
               [0.8, 1.7]]

    scatterY = [0.0, 0.0]

    xFormat = (-3.5, 3.5)
    yFormat = (0.0, 1.2)

    for i, sampleX in enumerate(samples):
        
        outname = filenames[i]
        outname += '_Python_' + platform.python_version() + \
                   '_mpl_' + mpl.__version__

        Xs = np.zeros((len(sampleX), 2))
        Xs[:, 0] = sampleX
        Xs[:, 1] = scatterY

        muML = mean_ML_estimator(Xs[:, 0])
        sigmaML = np.sqrt(variance_ML_estimator(Xs[:, 0]))
        yVals_inferred = norm.pdf(xVals, loc = muML, scale = sigmaML)
        X_inferred = np.zeros((n_vispoints, 2))
        X_inferred[:, 0] = xVals
        X_inferred[:, 1] = yVals_inferred

        # call the plotting function
        outname = Plot(X = X,
                       Xs = Xs,
                       X_inferred = X_inferred,
                       outname = outname,
                       outdir = OUTDIR,
                       pColors = pColors,
                       xFormat = xFormat,
                       yFormat = yFormat)

        cmd = 'pdf2svg ' + os.path.join(OUTDIR, outname + '.pdf') + \
          ' ' + os.path.join(OUTDIR, outname + '.svg')
        print(cmd)
        os.system(cmd)
