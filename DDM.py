# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:23:37 2018

@author: Max
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pypyodbc
import arcgis
from arcgis.features import *
os.chdir(r'D:\Projects\DrillingDataMaps')
from AGOcreds import *

from arcgis.gis import GIS
import json

gis = GIS("https://www.arcgis.com", AUSERNAME, APASSWORD)

# ALREADY ADDED USER-USER IN FILEMAKER
# NO SPACES IN CONNECTION STRING!!
cstr = 'DSN=FMMalcolm;Database=Malcolm Demo Max v2;UID=user;PWD=user'
db = pypyodbc.connect(cstr)

rawCoordinate = pd.read_sql(sql='SELECT * FROM Coordinate WHERE latitude IS NOT NULL AND longitude IS NOT NULL', con=db)
rawCoordinate.to_csv("rawCoord.csv")

df = rawCoordinate.copy()
df['SHAPE'] = df.apply(lambda row : arcgis.geometry.Geometry({'x': row['longitude'], 'y': row['latitude'], 'spatialReference':{'wkid':4326}}), axis=1 )
df['ptvalid'] = df.apply(lambda row : row['SHAPE'].is_valid, axis = 1)
sdf = SpatialDataFrame(df)
#layer = gis.content.import_data(sdf, title='Test3')
sdf.to_featureclass(out_location = r'D:\Projects\ORPHANS\ORPHANS.gdb', out_name = 'fctest8')


layer = gis.content.import_data(sdf, title='My Data')

 

m.add_layer(layer) # add to map

find_nearest(layer, ...) # use for analys

tt2 = r'D:\Projects\Bennett\Data\LukeDowning\Bennett Manhole As-Builts 13mar18 Coordinate List.csv'

