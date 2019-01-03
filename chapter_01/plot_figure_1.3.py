#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-01-03
# file: plot_figure_1.3.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 3.0.1
##########################################################################################

import os
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

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

def Plot(titlestr, X, Xs, params, outname, outdir, pColors, 
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
    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica'
    # the above two lines could also be replaced by the single line below
    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42  
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)     
    
    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 4.1, height = 3.2,
                       lFrac = 0.10, rFrac = 0.95, bFrac = 0.15, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    
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

    ax1.tick_params(axis='x', which='major', pad = 2.0)
    ax1.tick_params(axis='y', which='major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$x$', fontsize = 6.0, x = 0.98)
    # rotation (angle) is expressed in degrees
    ax1.set_ylabel(r'$t$', fontsize = 6.0, y = 0.82, rotation = 0.0)
    ax1.xaxis.labelpad = -6.5
    ax1.yaxis.labelpad = 5.0
    ######################################################################################
    # plotting
    
    lineWidth = 0.65    
    
    ax1.plot(X[:, 0], X[:, 1], 
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')
             
    ax1.scatter(Xs[:, 0], Xs[:, 1],
                s = 6.0,
                lw = lineWidth,
                facecolor = pColors[1],
                edgecolor = pColors[1],
                zorder = 3,
                label = r'')
    
    for i in range(Xs.shape[1]):
    
        ax1.plot([Xs[i, 0], Xs[i, 0]], [Xs[i, 1], Xs[i, 2]],
                 lw = lineWidth,
                 color = pColors[1])
                 
    ax1.scatter(Xs[:, 0], Xs[:, 2],
                s = 6.0,
                lw = lineWidth,
                facecolor = 'White',
                edgecolor = pColors[2],
                zorder = 4,
                label = r'')

    ######################################################################################
    # annotations
    
    label_1 = r'$t_n$'
    
    x_pos = 0.82
    
    ax1.annotate(label_1,
                 xy = (x_pos, 0.79),
                 xycoords = 'axes fraction',
                 fontsize = 6.0, 
                 horizontalalignment = 'left')

    label_2 = r'$y(x_n, \bf{w})$'
    
    ax1.annotate(label_2,
                 xy = (x_pos, 0.50),
                 xycoords = 'axes fraction',
                 fontsize = 6.0, 
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
    if (xFormat == None):
        pass
    else:
        ax1.set_xlim(xFormat[0], xFormat[1])
        ax1.set_xticks([Xs[2, 0]])
        ax1.set_xticklabels([r'$x_n$'])

    if (yFormat == None):
        pass
    else:
        ax1.set_ylim(yFormat[0], yFormat[1])
        ax1.set_yticklabels([])
        ax1.set_yticks([])
          
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

def modelFunc(x):
    
    return 0.05 * x ** 3 + 0.05 * x ** 2 + 0.05 * x
             
if __name__ == '__main__':
        
    # figure 1.3 - Bishop - Chapter 1 Introduction
    
    nVisPoints = 800
    xVals = np.linspace(-26.0, 24.0, nVisPoints)
    yVals = np.array([modelFunc(x) for x in xVals])
    
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    xPoints = np.array([-17.0, 4.0, 15.0])
    yModel = np.array([modelFunc(x) for x in xPoints])
    yData = np.array([modelFunc(xPoints[0]) + 700.0,
                      modelFunc(xPoints[1]) - 550.0,
                      modelFunc(xPoints[2]) + 640.0])
    
    Xs = np.zeros((len(xPoints), 3))
    Xs[:, 0] = xPoints
    Xs[:, 1] = yModel
    Xs[:, 2] = yData
    
    ######################################################################################
    # call the plotting function
    
    outname = 'prml_ch_01_figure_1.3'
    
    xFormat = [-29.0, 27.0]
    yFormat = [-1350.0, 1350.0]
    
    pColors = ['#FF0000', # standard red
               '#00FF00', # neon green
               '#0000FF'] # standard blue
    
    outname = Plot(titlestr = '',
                   X = X,
                   Xs = Xs,
                   params = [], 
                   outname = outname,
                   outdir = OUTDIR, 
                   pColors = pColors, 
                   grid = False, 
                   drawLegend = False, 
                   xFormat = xFormat,
                   yFormat = yFormat)
