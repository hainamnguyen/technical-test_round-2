# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 21:45:25 2017

@author: X1 Carbon
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np

def oned_plot(df1, criteria, condition):
    df = df1.copy()
    l = []
    fig = plt.figure()
    
    if criteria:
        for i in df:
            l.append([i, eval('df1[i].' + criteria + '()')])
        if condition:
            print('The skills with ' + criteria + ' ' + condition + ": ")
            for skill in sorted(l, key = lambda x: x[1], reverse = True):
                if eval('skill[1]' + condition):
                    print(skill)
        else:
            eval('df.' + criteria + '()').plot(kind='bar', figsize=(18, 15))
            plt.show()
            print('The first 10 skills with largest ' + criteria + ": ")
            for skill in sorted(l, key = lambda x: x[1], reverse = True)[:9]:
                print(skill)
    else: 
        for i in df: 
            df[i] = (eval('df[i]' + condition)) * 1
        df.sum().plot(kind='bar',figsize=(18, 15))
        plt.show()
        for i in df:
            l.append([i, df[i].sum()])
        print('The first 10 skills with largest number of employee ' + condition + ": ")
        for skill in sorted(l, key = lambda x: x[1], reverse = True)[:9]:
            print(skill)
            
def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1) 
                     * (x2 - x1) + x1)
        
    return sdata

class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360./len(variables))

        axes = [fig.add_axes([0.1,0.1,0.9,0.9],polar=True,
                label = "axes{}".format(i)) 
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles, 
                                         labels=variables, size = 20)
        [txt.set_rotation(angle-90) for txt, angle 
             in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], 
                               num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2)) 
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i])
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
        
    def plot(self, data, color,x_label, y_label, text, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw, c = color)
        self.ax.text(x_label, y_label, text,
        verticalalignment='bottom', horizontalalignment='right',
        transform=self.ax.transAxes,
        color=color, fontsize=15)
        
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
            
def rada_plot(df1, df2, variables):
    data = tuple([df1[i] for i in variables])
    data1 = tuple([df2[i] for i in variables])
    ranges = [(1, 6) for i in range(len(variables))]
    variables = tuple(variables)
    
    fig1 = plt.figure(figsize=(15, 15))
    radar = ComplexRadar(fig1, variables, ranges)
    radar.plot(data, color = 'r', x_label = 0.05, y_label =0.08, text= 'BEFORE')
    radar.fill(data, alpha=0.8)
    
    radar1 = ComplexRadar(fig1, variables, ranges)
    radar1.plot(data1, color = 'b', x_label = 0.05, y_label = 0.03, text= 'AFTER')
    radar1.fill(data1, alpha=0.8)
    plt.show()
    
    print('Improvement in each individual skills: ')
    for i in range(len(variables)):
        print(variables[i] + ' :', str(round((data1[i] - data[i])/data[i] * 100, 2)), '% ->', str(int(data1[i] - data[i])), 'step.')
    print('\nImprovement in total: ', str(round((sum(data1) - sum(data))/sum(data) * 100, 2)), '%')