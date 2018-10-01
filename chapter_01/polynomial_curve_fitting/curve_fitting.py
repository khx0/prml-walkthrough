#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-10-01
# file: curve_fitting.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################
import sys
import time
import datetime
import os
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(RAWDIR)
ensure_dir(OUTDIR)

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
    
def Plot(titlestr, X, Xt, Xm, params, outname, outdir, pColors, 
        grid = False, drawLegend = True, xFormat = None, yFormat = None, 
        savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font',**{'size': 10})
    mpl.rc('legend',**{'fontsize': 7.0})
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
                       lFrac = 0.10, rFrac = 0.95, bFrac = 0.15, tFrac = 0.95)
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
        
    xticks = plt.getp(plt.gca(), 'xticklines')
    yticks = plt.getp(plt.gca(), 'yticklines')
    ax1.tick_params('both', length = 1.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis='x', which='major', pad = 2.0)
    ax1.tick_params(axis='y', which='major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
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
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')
             
    ax1.scatter(Xt[:, 0], Xt[:, 1],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = pColors[1],
                zorder = 3,
                label = r'')

    ax1.plot(Xm[:, 0], Xm[:, 1], 
             color = pColors[2],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ######################################################################################
    # annotations
    
    label = r'$M = 3$'
    
    x_pos = 0.75
    
    ax1.annotate(label,
                 xy = (x_pos, 0.79),
                 xycoords = 'axes fraction',
                 fontsize = 5.0, 
                 horizontalalignment = 'left')
             
    ######################################################################################
    # legend
    if (drawLegend):
        leg = ax1.legend(#bbox_to_anchor = [0.7, 0.8],
                         #loc = 'upper left',
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
          
    ax1.set_axisbelow(False)
    for k, spine in ax1.spines.items():  #ax.spines is a dictionary
        spine.set_zorder(10)
    
    ######################################################################################
    # grid options
    if (grid):
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major', linewidth = 0.2)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor', linewidth = 0.1)
        ax1.grid('on', which = 'minor')
    ######################################################################################
    # save to file
    if (datestamp):
        outname += '_' + now
    if (savePDF):
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if (savePNG):
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

def poly_horner2(x, coeff):
    result = coeff[-1]
    for i in range(-2, -len(coeff)-1, -1):
        result = result * x + coeff[i]
    return result

if __name__ == '__main__':

    nVisPoints = 800
    xVals = np.linspace(0.0, 1.0, nVisPoints)
    yVals = np.array([np.sin(2.0 * np.pi * x) for x in xVals])
    
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
  
    # fix random number seed for reproducibility
    seedValue = 523456789
    seed = np.random.seed(seedValue)
    
    mu = 0.0
    sigma = 0.3
    
    # number of training data points
    # Xt = training data set
    # create nTrain training data points (here nTrain = 10)

    nTrain = 10
    
    Xt = np.zeros((nTrain, 2))
    xtVals = np.linspace(0.0, 1.0, nTrain)
    ytVals = np.array([np.sin(2.0 * np.pi * x) + np.random.normal(mu, sigma) 
                       for x in xtVals])
    Xt[:, 0] = xtVals
    Xt[:, 1] = ytVals
    
    ######################################################################################
    # file i/o
    
    outname = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_%d.txt' %(seedValue)
    
    np.savetxt(os.path.join(RAWDIR, outname), Xt, fmt = '%.8f')
    ######################################################################################
    
    
    ######################################################################################
    
    # polynomial least squares curve fitting
    
    m = 3 # degree of the fitting polynomial
    
    # fill the matrix
    A = np.ones((nTrain, m + 1))
    
    # column vector
    tmp = np.ones((nTrain,))
    
    for i in range(m):
        tmp = np.multiply(tmp, Xt[:, 0])
        A[:, i + 1] = tmp
    
    # fill the right hand side
    b = np.ones((nTrain, 1))
    b[:, 0] = Xt[:, 1]
    
    M = np.matmul(A.transpose(), A)
    b = np.matmul(A.transpose(), b)
        
    # solve linear system
    w = np.linalg.solve(M, b)
    w = w.reshape((m + 1,))
    print("Fitted parameters: ", w)
    
    ######################################################################################
    # create fitted model
    
    nModelPoints = 800
    xVals = np.linspace(0.0, 1.0, nModelPoints)
    yVals = np.array([poly_horner2(x, w) for x in xVals])
    Xm = np.zeros((nModelPoints, 2))
    Xm[:, 0] = xVals
    Xm[:, 1] = yVals
    
    ######################################################################################
    # file i/o
    
    outname = 'prml_ch_01_figure_1.2_training_data_PRNG-seed_%d_m_%d_fit.txt' \
              %(seedValue, m)
    
    np.savetxt(os.path.join(RAWDIR, outname), Xm, fmt = '%.8f')
    ######################################################################################
    
    ######################################################################################
    # call the plotting function
    
    outname = 'prml_ch_01_figure_1.4_PRNG-seed_%d_m_%d_fit_polynomial_leastSq' \
              %(seedValue, m)
    
    xFormat = [-0.05, 1.05, 0.0, 1.1, 1.0, 1.0]
    yFormat = [-1.35, 1.35, -1.0, 1.1, 1.0, 1.0]
        
    pColors = ['#00FF00', # neon green
               '#0000FF', # standard blue
               '#FF0000'] # standard red
    
    outname = Plot(titlestr = '',
                   X = X,
                   Xt = Xt,
                   Xm = Xm,
                   params = [], 
                   outname = outname,
                   outdir = OUTDIR, 
                   pColors = pColors, 
                   grid = False, 
                   drawLegend = False, 
                   xFormat = xFormat,
                   yFormat = yFormat)
    
    
    
