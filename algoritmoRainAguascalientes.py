#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 08:38:15 2017

@author: jorgemauricio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata as gd

#%% read csv
data1 = pd.read_table('data/d1.txt', sep=',')
data2 = pd.read_table('data/d2.txt', sep=',')
data3 = pd.read_table('data/d3.txt', sep=',')
data4 = pd.read_table('data/d4.txt', sep=',')
data5 = pd.read_table('data/d5.txt', sep=',')

#%% make one dataFrame
data = data1.filter(items=['Long', 'Lat','Rain'])
data['Rain2'] = data2['Rain']
data['Rain3'] = data3['Rain']
data['Rain4'] = data4['Rain']
data['Rain5'] = data5['Rain']
data['Acum'] = data['Rain'] + data['Rain2'] + data['Rain3'] + data['Rain4'] + data['Rain5']

#%% get values from Ags
data = data.loc[data['Lat'] > 21.0]
data = data.loc[data['Lat'] < 24.0]
data = data.loc[data['Long'] > -104.0]
data = data.loc[data['Long'] < -100.0]

#%% get x and y values
lons = np.array(data['Long'])
lats = np.array(data['Lat'])

#%% set up plot
plt.clf()
#fig = plt.figure(figsize=(48,24))
m = Basemap(projection='mill',llcrnrlat=21.3,urcrnrlat=23,llcrnrlon=-103.5,urcrnrlon=-101,resolution='h')

#%% generate lats, lons
x, y = m(lons,lats)

#%% number of cols and rows
numcols = len(x)
numrows = len(y)

#%% generate xi, yi
xi = np.linspace(x.min(), x.max(), numcols)
yi = np.linspace(y.min(), y.max(), numrows)

#%% generate meshgrid
xi, yi = np.meshgrid(xi,yi)

#%% genate zi
z = np.array(data['Rain'])
zi = gd((x,y), z, (xi,yi), method='linear')

#%% contour plot
cs = m.contourf(xi,yi,zi, zorder=4, alpha=0.5, cmap='RdPu')
#%% draw map details
m.drawcoastlines()
m.drawstates(linewidth=0.7)
m.drawcountries()
#m.drawmapscale(22, -103, 23, -102, 100, units='km', fontsize=14, yoffset=None, barstyle='fancy', labelstyle='simple', fillcolor1='w', fillcolor2='#000000',fontcolor='#000000', zorder=5)

#%% # add colour bar and title
cbar = m.colorbar(cs, location='right', pad="5%")
cbar.set_label('mm')
plt.title('Precipitación')
plt.savefig('maps/precipitacion.png', dpi=300, transparent=True)
plt.show()
