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
from time import gmtime, strftime
import time

#%% fecha del pronostico
fechaPronostico = strftime("%Y-%m-%d")

#%% read csv
data1 = pd.read_table('data/d1.txt', sep=',')
data2 = pd.read_table('data/d2.txt', sep=',')
data3 = pd.read_table('data/d3.txt', sep=',')
data4 = pd.read_table('data/d4.txt', sep=',')
data5 = pd.read_table('data/d5.txt', sep=',')

#%% make one dataFrame
data = data1.filter(items=['Long', 'Lat','Rain'])
data['Rain1'] = data1['Rain']
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

#%% generate arrayFechas
# Generate Days
arrayFechas = []
tanio, tmes, tdia = fechaPronostico.split('-')
anio = int(tanio)
mes = int(tmes)
dia = int(tdia)

for i in range(0,5,1):
	if i == 0:
		newDiaString = '{}'.format(dia)
		if len(newDiaString) == 1:
			newDiaString = '0' + newDiaString
		newMesString = '{}'.format(mes)
		if len(newMesString) == 1:
			newMesString = '0' + newMesString
		fecha = '{}'.format(anio)+"-"+newMesString+"-"+newDiaString
		arrayFechas.append(fecha)
	if i > 0:
		dia = dia + 1
		if mes == 2 and anio % 4 == 0:
			diaEnElMes = 29
		elif mes == 2 and anio % 4 != 0:
			diaEnElMes = 28
		elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
			diaEnElMes = 31
		elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
			diaEnElMes = 30
		if dia > diaEnElMes:
			mes = mes + 1
			dia = 1
		if mes > 12:
			anio = anio + 1
			mes = 1
		newDiaString = '{}'.format(dia)
		if len(newDiaString) == 1:
			newDiaString = '0' + newDiaString
		newMesString = '{}'.format(mes)
		if len(newMesString) == 1:
			newMesString = '0' + newMesString
		fecha = '{}'.format(anio)+"-"+newMesString+"-"+newDiaString
		arrayFechas.append(fecha)

#%% loop diarios
counterFecha = 0
for i in range(1,6,1):
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
	tempTitleColumn = "Rain{}".format(i)
	z = np.array(data[tempTitleColumn])
	zi = gd((x,y), z, (xi,yi), method='cubic')

	#%% generate clevs
	def generateClevs(minV, maxV):
		arrayValues = []
		step = (maxV - minV) / 10
		for i in range(10):
			rangeOfValue = int(step * i)
			arrayValues.append(rangeOfValue)
		return arrayValues

	clevs = generateClevs(z.min(), z.max())
	#%% contour plot
	cs = m.contourf(xi,yi,zi, clevs, zorder=4, alpha=0.5, cmap='Spectral_r')
	#%% draw map details
	m.drawcoastlines()
	#m.drawstates(linewidth=0.7)
	m.drawcountries()
	#%% read municipios shape file
	m.readshapefile('shapes/Municipios', 'Municipios')
	#m.readshapefile('shapes/Estados', 'Estados')
	#m.drawmapscale(22, -103, 23, -102, 100, units='km', fontsize=14, yoffset=None, barstyle='fancy', labelstyle='simple', fillcolor1='w', fillcolor2='#000000',fontcolor='#000000', zorder=5)

	#%% colorbar
	cbar = m.colorbar(cs, location='right', pad="5%")
	cbar.set_label('mm')
	tempMapTitle = "Precipitación acumulada en 24h (mm)\nPronóstico válido para: {}".format(arrayFechas[counterFecha])
	plt.title(tempMapTitle)
	tempFileName = "maps/{}.png".format(arrayFechas[counterFecha])
	plt.annotate('INIFAP (WRF -EMS)', xy=(-102,22), xycoords='data', xytext=(-102,21), color='g')
	plt.savefig(tempFileName, dpi=300, transparent=True)
	counterFecha += 1
	print('****** Genereate: {}'.format(tempFileName))

#%% generate Acum
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
z = np.array(data['Acum'])
zi = gd((x,y), z, (xi,yi), method='cubic')

#%% generate clevs
def generateClevs(minV, maxV):
	arrayValues = []
	step = (maxV - minV) / 10
	for i in range(10):
		rangeOfValue = int(step * i)
		arrayValues.append(rangeOfValue)
	return arrayValues

clevs = generateClevs(z.min(), z.max())
#%% contour plot
cs = m.contourf(xi,yi,zi, clevs, zorder=4, alpha=0.5, cmap='Spectral_r')
#%% draw map details
m.drawcoastlines()
#m.drawstates(linewidth=0.7)
m.drawcountries()
#%% read municipios shape file
m.readshapefile('shapes/Municipios', 'Municipios')
#m.readshapefile('shapes/Estados', 'Estados')
#m.drawmapscale(22, -103, 23, -102, 100, units='km', fontsize=14, yoffset=None, barstyle='fancy', labelstyle='simple', fillcolor1='w', fillcolor2='#000000',fontcolor='#000000', zorder=5)

#%% colorbar
cbar = m.colorbar(cs, location='right', pad="5%")
cbar.set_label('mm')
tempMapTitle = "Precipitación acumulada en 24h (mm)\nPronóstico válido para {} al {}".format(arrayFechas[0],arrayFechas[-1])
plt.title(tempMapTitle)
plt.annotate('INIFAP (WRF -EMS)', xy=(-102,22), xycoords='data', xytext=(-102,21), color='g')
plt.savefig("maps/acum.png", dpi=300, transparent=True)
print('****** Genereate: Acum')