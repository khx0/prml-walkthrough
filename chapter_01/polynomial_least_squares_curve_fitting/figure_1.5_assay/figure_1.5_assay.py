#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-24
# file: figure_1.5_assay
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.3
##########################################################################################

import sys
sys.path.append('../')
sys.path.append('../../../lib')
import os
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from matplotlib.ticker import FuncFormatter

from polynomials import polynomial_horner

from polyLeastSquares import polyLeastSquares

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)
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

def Plot(titlestr, X, outname, outdir, pColors, 
         grid = False, drawLegend = True, xFormat = None, yFormat = None, 
         savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    
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
        getFigureProps(width = 4.1, height = 2.9,
                       lFrac = 0.18, rFrac = 0.95,
                       bFrac = 0.18, tFrac = 0.95)
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
    
    ax1.tick_params(axis = 'x', which = 'major', pad = 3.5)
    ax1.tick_params(axis = 'y', which = 'major', pad = 3.5, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$M$', fontsize = 6.0)
    ax1.set_ylabel(r'$E_{\mathrm{RMS}}$', fontsize = 6.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0 
    ######################################################################################
    # plotting
    
    lineWidth = 0.65    
    
    # plot test error
    ax1.plot(X[:, 0], X[:, 2], 
             color = pColors['red'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 11,
             label = r'',
             clip_on = False)
    
    ax1.scatter(X[:, 0], X[:, 2],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = pColors['red'],
                zorder = 11,
                label = r'Test',
                clip_on = False)
    
    # plot training error
    ax1.plot(X[:, 0], X[:, 1], 
             color = pColors['blue'],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 11,
             label = r'',
             clip_on = False)
    
    ax1.scatter(X[:, 0], X[:, 1],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = pColors['blue'],
                zorder = 11,
                label = r'Training',
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
    
    # PRML Bishop chapter 1 Introduction - Curve Fitting - figure 1.5 assay
    
    ######################################################################################
    # global parameters
    nTrain = 10
    nTest = 100
    
    # noise settings
    # numpy.random.normal() function signature:
    # numpy.random.normal(loc = 0.0, scale = 1.0, size = None)
    # loc = mean ($\mu$)
    # scale = standard deviation ($\sigma$)
    # $\mathcal{N}(\mu, \sigma^2)$
    mu = 0.0
    sigma = 0.3
    
    # fix random number seed for reproducibility
    # seedValue = 123456789 gives a nice figure like fig. 1.5 in the book
    seedValue = 123456789
    seed = np.random.seed(seedValue)
    
    ######################################################################################
    # create training data
    Xt = np.zeros((nTrain, 2))
    xVals = np.linspace(0.0, 1.0, nTrain)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape)
    Xt[:, 0] = xVals
    Xt[:, 1] = yVals
    
    ######################################################################################
    # create test data
    xVals = np.linspace(0.0, 1.0, nTest)
    yVals = np.sin(2.0 * np.pi * xVals) + np.random.normal(mu, sigma, xVals.shape)    
    X = np.zeros((nTest, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    ######################################################################################
    # polynomial curve fitting (learning the model)
        
    mOrder = np.arange(0, 10, 1).astype('int')
    res = np.zeros((len(mOrder), 3))
    
    for m in mOrder:
        
        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))
        
        # polynomial least square curve fitting
        w = polyLeastSquares(m, Xt)
        
        yPredict = polynomial_horner(Xt[:, 0], *w)
        
        # test data set prediction
        yPredictTest = polynomial_horner(X[:, 0], *w)
        
        # compute sum of squares deviation
        
        sum_of_squares_error = 0.5 * np.sum(np.square(yPredict - Xt[:, 1]))
        sum_of_squares_error_test = 0.5 * np.sum(np.square(yPredictTest - X[:, 1]))
        
        RMS = np.sqrt(2.0 * sum_of_squares_error / nTrain)
        RMS_test = np.sqrt(2.0 * sum_of_squares_error_test / nTest)
        
        res[m, 0] = m
        res[m, 1] = RMS
        res[m, 2] = RMS_test
    
    ######################################################################################
    # file i/o
    outname = 'figure_1.5_data_PRNG-seed_%d.txt' %(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname), res, fmt = '%.8f')
    ######################################################################################
    
    ######################################################################################
    # call the plotting function
    
    outname = 'prml_ch_01_figure_1.5_PRNG-seed_%d' %(seedValue)
    
    xFormat = [-0.5, 9.5, 0.0, 9.1, 3.0, 1.0]
    yFormat = [0.0, 1.00, 0.0, 1.05, 0.5, 0.5]
    
    pColors = {'blue': '#0000FF',   # standard blue
               'red': '#FF0000'}    # standard red
        
    outname = Plot(titlestr = '',
                   X = res,
                   outname = outname,
                   outdir = OUTDIR, 
                   pColors = pColors, 
                   grid = False, 
                   drawLegend = True, 
                   xFormat = xFormat,
                   yFormat = yFormat)
