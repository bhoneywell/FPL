#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:30:41 2020

@author: wellhoneyb
"""

##Code to predict players FPL points per gw based on previous season's performance

import pandas as pd
url = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/gws/merged_gw.csv'
df = pd.read_csv(url)
##print(df.head())

## pulling predictors we'd have access to before the season as well as the response variable total_points

predictionData = df[['name','kickoff_time','opponent_team','total_points','GW']]
print(predictionData.head())