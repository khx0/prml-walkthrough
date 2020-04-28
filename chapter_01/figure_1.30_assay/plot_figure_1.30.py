#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-04-28
# file: plot_figure_1.30.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.1
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from scipy.stats import norm

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def cleanFormatter(x, pos = None):
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

def Plot(bins, values, outname, outdir, pColors, labelString = None,
         titlestr = None, params = None, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

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
        getFigureProps(width = 6.6, height = 6.6,
                       lFrac = 0.16, rFrac = 0.95,
                       bFrac = 0.05, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac,
                      right = rFrac)
    f.subplots_adjust(bottom = bFrac,
                      top = tFrac)

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
    ax1.set_xlabel(r'', fontsize = 8.0, x = 0.95)
    ax1.set_ylabel(r'probabilities', fontsize = 8.0)
    ax1.xaxis.labelpad = 0.0
    ax1.yaxis.labelpad = 8.0
    ######################################################################################
    # plotting

    # This way of calling mpl's hist function is suitable for plotting already
    # binned data, as it is the case here.
    ax1.hist(bins[:-1], bins, weights = values,
             color = pColors['opaque_standard_blue'],
             edgecolor = 'k',
             linewidth = 1.0)

    ######################################################################################
    # annotations
    if labelString:
        x_pos, y_pos = 0.5, 0.65
        ax1.annotate(labelString,
                     xy = (x_pos, y_pos),
                     xycoords = 'axes fraction',
                     fontsize = 10.0,
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

    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)

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
    Computes the discrete sample entropy of the given
    probabilities x.
    '''
    H = 0.0
    for pi in x:
        if np.isclose(pi, 0.0):
            continue
        else:
            H += -pi * np.log(pi)
    return H

######################################################################################
# sample probability values from normal distribution
# scipy.stats.norm(x, loc, scale)
# IMPORTANT: Scipy's norm.pdf() takes the standard deviation and
# not the variance as scale parameter. This is one of the most frequent pitfalls
# when using normal distributions.
######################################################################################

######################################################################################
# color settings
# #0000FF = RGB(0, 0, 255)
# #6666ff roughly corresponds to #0000FF at 0.55 opacity
# plot color dictionary
pColors = {'blue': '#0000FF',
           'opaque_standard_blue': '#6666ff'
           }
######################################################################################

if __name__ == '__main__':

    # figure 1.30 Bishop - Chapter 1 Introduction

    ##################################################################################
    # create data for figure 1.30 left
    xmin, xmax = 0.0, 1.0
    nBins = 30
    dx = (xmax - xmin) / float(nBins)
    bins = np.linspace(xmin, xmax, nBins + 1)
    binCenters = bins[:-1] + dx / 2.0

    pValues = np.zeros((nBins,))
    selectorSet = [10, 11, 12, 13, 14, 15, 16, 17, 18]

    pValues[selectorSet] = norm.pdf(binCenters[selectorSet],
                                    loc = binCenters[14],
                                    scale = 0.048)

    # normalize the discrete probability distribution
    normalization = np.sum(pValues)
    pValues /= normalization

    assert np.isclose(np.sum(pValues), 1.0), "Error: Normalization assertion failed."

    H_value = entropy(pValues)

    # plotting

    xFormat = (0.0, 1.0)
    yFormat = (0.0, 0.5, 0.0, 0.55, 0.25, 0.25)

    outname = 'prml_ch_01_figure_1.30_left'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(bins = bins,
                   values = pValues,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = rf'$H={H_value:.3}$',
                   xFormat = xFormat,
                   yFormat = yFormat)

    ##################################################################################
    # create data for figure 1.30 right
    xmin, xmax = 0.0, 1.0
    nBins = 30
    dx = (xmax - xmin) / float(nBins)
    bins = np.linspace(xmin, xmax, nBins + 1)
    binCenters = bins[:-1] + dx / 2.0

    pValues = np.zeros((nBins,))
    pValues = norm.pdf(binCenters,
                       loc = binCenters[14],
                       scale = 0.184)

    # normalize the discrete probability distribution
    normalization = np.sum(pValues)
    pValues /= normalization

    assert np.isclose(np.sum(pValues), 1.0), "Error: Normalization assertion failed."

    H_value = entropy(pValues)

    # plotting

    xFormat = (0.0, 1.0)
    yFormat = (0.0, 0.5, 0.0, 0.55, 0.25, 0.25)

    outname = 'prml_ch_01_figure_1.30_right'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(bins = bins,
                   values = pValues,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = rf'$H={H_value:.3}$',
                   xFormat = xFormat,
                   yFormat = yFormat)

    ##################################################################################
    # create data for a uniform distribution on the same x-grid
    xmin, xmax = 0.0, 1.0
    nBins = 30
    dx = (xmax - xmin) / float(nBins)
    bins = np.linspace(xmin, xmax, nBins + 1)
    binCenters = bins[:-1] + dx / 2.0

    pValues = 1.0 / float(nBins) * np.ones((nBins,))

    assert np.isclose(np.sum(pValues), 1.0), "Error: Normalization assertion failed."

    H_value = entropy(pValues)

    # plotting
    xFormat = (0.0, 1.0)
    yFormat = (0.0, 0.5, 0.0, 0.55, 0.25, 0.25)

    outname = 'prml_ch_01_figure_1.30_uniform'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(bins = bins,
                   values = pValues,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = rf'$H={H_value:.3}$',
                   xFormat = xFormat,
                   yFormat = yFormat)
