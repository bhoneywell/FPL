#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:30:41 2020

@author: wellhoneyb
"""

##Code to predict players FPL points per gw based on previous season's performance

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
import re


url = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/gws/merged_gw.csv'
df = pd.read_csv(url)
##print(df.head())

def pull_hour(kickoff_time):
    kickoff_time = re.sub('[A-Z]', ' ', kickoff_time)  
    date_time_obj = datetime.strptime(kickoff_time, '%Y-%m-%d %H:%M:%S ')
    return(date_time_obj.hour)

## pulling predictors we'd have access to before the season as well as the response variable total_points

df = df[['name','kickoff_time','opponent_team','total_points','GW']]
df['name'] =df['name'].apply(lambda x: x[:-4].replace('_',' '))
df['kickoff_hour'] = df['kickoff_time'].apply(lambda x: pull_hour(x))
print(df.head())


## Need to parameterize if making a GUI
player_model = df[df['name'] == 'Aaron Wan-Bissaka']

#print(player_model)
#print(player_model[['kickoff_hour','opponent_team','GW']])

X = player_model[['kickoff_hour','opponent_team','GW']]
y = player_model['total_points']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)
lm = LinearRegression()
lm.fit(X_train,y_train)

print(lm.intercept_)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(coeff_df)
print(coeff_df.loc['kickoff_hour','Coefficient'])