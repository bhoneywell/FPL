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
        playerLabel.grid(row = 0, column =0, columnspan = 2)
        self.sv = StringVar()
        options = self.df['name'].unique().tolist()
        playerMenu = OptionMenu(rootWin, self.sv, *options, command=self.player_selected)
        playerMenu.grid(row = 1, column = 0, columnspan = 2)
        
    def pull_hour(self,kickoff_time):
        kickoff_time = re.sub('[A-Z]', ' ', kickoff_time)  
        date_time_obj = datetime.strptime(kickoff_time, '%Y-%m-%d %H:%M:%S ')
        return(date_time_obj.hour)
    
    def df_cleanup(self):
        self.df = df[['name','kickoff_time','opponent_team','total_points','GW']]
        self.df['name'] =df['name'].apply(lambda x: x[:-4].replace('_',' '))
        self.df['kickoff_hour'] = df['kickoff_time'].apply(lambda x: self.pull_hour(x))
        #print(self.df.head())
        
    def player_selected(self):
        pass
        
        
        
        
        
        
rootWin = Tk()
app = fpl_predictor(rootWin)
rootWin.mainloop()