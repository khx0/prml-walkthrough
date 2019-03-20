#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-10-19
# file: curve_fitting_training_error_variety.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 2.2.3
##########################################################################################

import sys
sys.path.append('../lib')
import datetime
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

from scipy.optimize import curve_fit

from polynomials import polynomial_horner

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'prml_ch_01_figure_1.5_variety')

ensure_dir(OUTDIR)
ensure_dir(RAWDIR)

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
                       lFrac = 0.18, rFrac = 0.95, bFrac = 0.18, tFrac = 0.95)
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

    ax1.tick_params(axis='x', which='major', pad = 3.5)
    ax1.tick_params(axis='y', which='major', pad = 3.5, zorder = 10)
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
        
    ax1.plot(X[:, 0], X[:, 1], 
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 11,
             label = r'',
             clip_on = False)
             
    ax1.scatter(X[:, 0], X[:, 1],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = pColors[0],
                zorder = 11,
                label = r'Training',
                clip_on = False)
             
    ######################################################################################
    # legend
    if drawLegend:
        leg = ax1.legend(# bbox_to_anchor = [0.7, 0.8],
                         # loc = 'upper left',
                         handlelength = 0.05, 
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
        
        ###########################################
        # manual y ticks
        print("ATTENTION: MANUAL Y TICKS USED.")
        ax1.set_yticklabels([0, 0.5, 1])
        ###########################################
        
    ax1.set_axisbelow(False)
    
    for spine in ax1.spines.values():  # ax1.spines is a dictionary
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

def createTrainingData(N, mu, sigma):
    # Xt = training data set
    xtVals = np.linspace(0.0, 1.0, N)
    ytVals = np.sin(2.0 * np.pi * xtVals) + np.random.normal(mu, sigma, xtVals.shape) 
    # create N training data points (N = 10)
    Xt = np.zeros((N, 2))
    Xt[:, 0] = xtVals
    Xt[:, 1] = ytVals
    return Xt

def polynomialCurveFitting(mOrder, Xt):
    
    res = np.zeros((len(mOrder), 2))
    
    for m in mOrder:
        
        # create coefficient vector (containing all fit parameters)
        w = np.ones((m + 1,))
        
        # curve fitting
        popt, pcov = curve_fit(polynomial_horner, Xt[:, 0], Xt[:, 1], p0 = w)
        
        yPredict = polynomial_horner(Xt[:, 0], *popt)
        
        # compute sum of squares deviation
        
        sum_of_squares_error = 0.5 * np.sum(np.square(yPredict - Xt[:, 1]))
        
        RMS = np.sqrt(2.0 * sum_of_squares_error / N)
        
        res[m, 0] = m
        res[m, 1] = RMS
    
    return res

if __name__ == '__main__':

    # global plot settings
    xFormat = [-0.5, 9.5, 0.0, 9.1, 3.0, 1.0]
    yFormat = [0.0, 1.00, 0.0, 1.05, 0.5, 0.5]
    pColors = ['#0000FF'] # standard blue
    
    tries = 40
    np.random.seed(123456789)
    
    for i in range(tries):
    
        outname = 'prml_ch_01_figure_1.5_training_error_only_variety_id_%s' \
                  %(str(i + 1).zfill(2))
        
        # create training data
        N = 10
        mu = 0.0
        sigma = 0.3
        Xt = createTrainingData(N, mu, sigma)
        N = Xt.shape[0]
        print("Training data shape =", Xt.shape)
        print("number of training data points N =", N)
        
        # polynomial curve fitting
        mOrder = np.arange(0, 10, 1).astype('int')
        Et = polynomialCurveFitting(mOrder, Xt)
        
        # call the plotting function
        outname = Plot(titlestr = '',
                       X = Et,
                       outname = outname,
                       outdir = OUTDIR, 
                       pColors = pColors, 
                       grid = False, 
                       drawLegend = True, 
                       xFormat = xFormat,
                       yFormat = yFormat)
