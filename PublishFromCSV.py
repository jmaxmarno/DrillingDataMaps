# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 13:23:41 2018

@author: Max
"""
import time
import os
import pandas as pd
import numpy as np
import pypyodbc
import arcgis
from arcgis.features import *
os.chdir(r'D:\Projects\DrillingDataMaps')
from AGOcreds import *

from arcgis.gis import GIS
import json

t=time.process_time()

# AGO USERNAME AND PW
gis = GIS("https://www.arcgis.com", AUSERNAME, APASSWORD)

# CONNECT TO FILEMAKER DB VIA ODBC CONNECTION
'''
	• Install FM Pro
	• Enable sharing 
		○ File>Sharing>Enable ODBC/JDBC
			§ On
			§ All users, or specify
				□ Create 'user' profile as the odbc connection will always ask for username and pw, ie user, user
	• Install ODBC driver
		○ Located in the folder where the .exe installer was extracted (usually downloads)
		○ Run 'ODBC Data Source Administrator'
			§ FileMaker Pro/ the database must be open when setting up this connection
			§ Add System DSN
				□ FileMaker ODBC
				□ Use same title for Name and Description
				□ !!!Make 'Describe text fields as long varchar' is checked
	• Access database using pypyodbc
		cstr = 'DSN=FMMalcolm;Database=Malcolm DEMO Max v2;UID=user;PWD=user'
		db = pypyodbc.connect(cstr)
'''

cstr = 'DSN=FMMalcolm;Database=Malcolm Demo Max v2;UID=user;PWD=user'
db = pypyodbc.connect(cstr)
# READ FILEMAKER TABLE TO PANDAS DATAFRAME (SQL)
# Coordinate TABLE
rawCoordinate = pd.read_sql(sql='SELECT * FROM Coordinate WHERE latitude IS NOT NULL AND longitude IS NOT NULL', con=db)

#rawCoordinate.loc[:,'name'] = 'MAX'
# ADD PDF URL:
rawCoordinate['PDFurl'] =  rawCoordinate.apply(lambda row : 'https://api.bohrlog.guh-messtec.de/api/pdf/{}'.format(str(row['fileid'])), axis=1)

# WRITE DATAFRAME TO CSV
rawCoordinate.to_csv("rawCoord.csv")
# CSV PATH
RCcsv = r'D:\Projects\DrillingDataMaps\rawCoord.csv'

#csv_item = gis.content.add({}, RCcsv)
#csv_lyr = csv_item.publish(overwrite = True)

# PUBLISH NEW LAYER IF NOT EXISTS
# ELSE OVERWRITE (FIRST DELETING CSV REF DATA)
search_results_layer = gis.content.search('title:rawCoord, type:Feature Service')
if len(search_results_layer) != 0:
    print('RawCoord already exists! Deleting csv and updating data...')
    search_results = gis.content.search('title:rawCoord, type:CSV')
    tooverwrite = search_results[0]
    tooverwrite.delete()
    
    csv_item = gis.content.add({}, RCcsv)
    csv_lyr = csv_item.publish(overwrite = True)
else:
    print('Publishing from scratch!')
    csv_item = gis.content.add({}, RCcsv)
    csv_lyr = csv_item.publish()
elapsedtime = time.process_time()-t
print(elapsedtime)





search_results = gis.content.search('title:rawCoord')
for i in search_results:
    i.delete()
tooverwrite = search_results[0]
tooverwrite.delete()
