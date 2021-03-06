#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-24
# file: figure_1.6_assay_N_300.py
# tested with python 3.7.6 in conjunction with mpl 3.3.3
##########################################################################################

# noise settings
# numpy.random.normal() function signature:
# numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
# loc = mean ($\mu$)
# scale = standard deviation ($\sigma$)
# $\mathcal{N}(\mu, \sigma^2)$

import sys
sys.path.append('../../lib')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

from scipy.optimize import curve_fit

from polynomials import polynomial_horner

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

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

def Plot(X, Xt, Xm, params, outname, outdir, pColors, titlestr = None,
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
    # rotation is expressed in degrees
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
                zorder = 1,
                label = r'')

    ax1.plot(Xm[:, 0], Xm[:, 1],
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ######################################################################################
    # annotations

    label = r'$M = 9$'

    x_pos = 0.80

    ax1.annotate(label,
                 xy = (x_pos, 0.89),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

    label = r'$N = %d$' %(params[0])

    ax1.annotate(label,
                 xy = (x_pos, 0.79),
                 xycoords = 'axes fraction',
                 fontsize = 5.0,
                 horizontalalignment = 'left')

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

    # PRML Bishop chapter 1 Introduction - Curve Fitting - figure 1.6 assay

    # global parameters
    n_train = 300

    mu = 0.0
    sigma = 0.3

    ######################################################################################
    seed_value = 923456789
    # The seed_value = 923456789 gives a nice result for N = 300
    # training data points.
    ######################################################################################

    ######################################################################################
    # fix random number seed for reproducibility
    np.random.seed(seed_value)
    ######################################################################################
    n_vispoints = 800
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    yVals = np.sin(2.0 * np.pi * xVals)

    # X = ground truth
    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    ######################################################################################
    # create training data
    xVals = np.linspace(0.0, 1.0, n_train)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape)
    Xt = np.zeros((n_train, 2))
    Xt[:, 0] = xVals
    Xt[:, 1] = yVals

    ######################################################################################
    # file i/o
    outname = f'figure_1.6_training_data_N_{n_train}_PRNG_seed_{seed_value}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), Xt, fmt = '%.8f')
    ######################################################################################

    ######################################################################################
    # polynomial curve fitting (learning the model)
    m = 9
    w = np.ones((m + 1,))
    popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)

    # create fitted model
    n_modelpoints = 800
    xVals = np.linspace(0.0, 1.0, n_modelpoints)
    yVals = polynomial_horner(xVals, *popt)
    Xm = np.zeros((n_modelpoints, 2))
    Xm[:, 0] = xVals
    Xm[:, 1] = yVals

    ######################################################################################
    # file i/o
    outname = f'figure_1.6_fitted_model_N_{n_train}_PRNG_seed_{seed_value}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), X, fmt = '%.8f')
    ######################################################################################

    ######################################################################################
    # call the plotting function

    outname = f'figure_1.6_N_{n_train}_PRNG_seed_{seed_value}'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xFormat = (-0.05, 1.05, 0.0, 1.1, 1.0, 1.0)
    yFormat = (-1.7, 1.7, -1.0, 1.1, 1.0, 1.0)

    pColors = {'green': '#00FF00', # neon green
               'blue': '#0000FF',  # standard blue
               'red': '#FF0000'}   # standard red

    outname = Plot(X = X,
                   Xt = Xt,
                   Xm = Xm,
                   params = [n_train],
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   xFormat = xFormat,
                   yFormat = yFormat)
