#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:56:18 2020

@author: wellhoneyb
"""


from tkinter import *
import tkinter as tk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
import re

url = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/gws/merged_gw.csv'
df = pd.read_csv(url)

class fpl_predictor:
    def __init__(self,master):
        self.win = rootWin
        self.df_cleanup()
        self.home_page()
        
        
        
    def home_page(self):
        self.win.title("FPL Home")
        playerLabel = Label(self.win, text="Select your FPL player:")
        playerLabel.grid(row = 0, column =0, columnspan = 3)
        self.sv = StringVar()
        options = self.df['name'].unique().tolist()
        playerMenu = OptionMenu(self.win, self.sv, *options, command=self.player_selected)
        playerMenu.grid(row = 1, column = 0, columnspan = 2)
        
        
    def pull_hour(self,kickoff_time):
        kickoff_time = re.sub('[A-Z]', ' ', kickoff_time)  
        date_time_obj = datetime.strptime(kickoff_time, '%Y-%m-%d %H:%M:%S ')
        return(date_time_obj.hour)
    
    def df_cleanup(self):
        self.df = df[['name','kickoff_time','opponent_team','total_points','GW']]
        self.df['name'] =self.df['name'].apply(lambda x: x[:-4].replace('_',' '))
        self.df['kickoff_hour'] = self.df['kickoff_time'].apply(lambda x: self.pull_hour(x))
        print(self.df)
        #print(self.df.head())
        
    def player_selected(self,playerName):
        print(playerName)
        print(len(playerName))
        playerName.strip()
        player_model = self.df[self.df['name'] == playerName]
        print(player_model)
        X = player_model[['kickoff_hour','opponent_team','GW']]
        y = player_model['total_points']


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)
        lm = LinearRegression()
        lm.fit(X_train,y_train)

        intercept = (lm.intercept_)
        coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
        print(coeff_df)
        kickoff_coeff = coeff_df.loc['kickoff_hour','Coefficient']
        team_coeff = coeff_df.loc['opponent_team','Coefficient']
        gw_coeff = coeff_df.loc['GW','Coefficient']
        eqn = "points = {}kickoff_hour + {}opponent_team + {}GW + {}".format(kickoff_coeff,team_coeff,gw_coeff,intercept)
        print(eqn)
        #equationLabel = Label(self.win, text = )
        
        
        
        
        
        
rootWin = Tk()
app = fpl_predictor(rootWin)
rootWin.mainloop()