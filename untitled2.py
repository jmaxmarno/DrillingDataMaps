%reset-f
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

cstr = 'DSN=FMMalcolm;Database=Malcolm Demo Max v2;UID=user;PWD=user'
db = pypyodbc.connect(cstr)

rawCoordinate = pd.read_sql(sql='SELECT * FROM Coordinate WHERE latitude IS NOT NULL AND longitude IS NOT NULL', con=db)
#rawCoordinate.to_csv("rawCoord.csv")
df = rawCoordinate.copy()

keepers = ['latitude', 'longitude', 'name', 'fips']
df2= df[keepers].copy()
keepers = ['latitude', 'longitude', 'name', 'fips']
df2= df[keepers].copy()


df2['SHAPE'] = df2.apply(lambda row : arcgis.geometry.Geometry({'x': row['longitude'], 'y': row['latitude'], 'spatialReference':{'wkid':2346}}), axis=1 )
#df2['ptvalid'] = df2.apply(lambda row : row['SHAPE'].is_valid, axis = 1)
sdf = SpatialDataFrame(df2)

sdf.to_featurelayer(title= 'pddrettyplease', gis=gis)
