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

        self.kickVar = StringVar()
        self.opponentVar = StringVar()
        self.gwVar = StringVar()


        self.intercept = (lm.intercept_)
        coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
        print(coeff_df)
        self.kickoff_coeff = coeff_df.loc['kickoff_hour','Coefficient']
        self.team_coeff = coeff_df.loc['opponent_team','Coefficient']
        self.gw_coeff = coeff_df.loc['GW','Coefficient']
        self.eqn = "points = {}kickoff_hour + {}opponent_team + {}GW + {}".format(self.kickoff_coeff,self.team_coeff,self.gw_coeff,self.intercept)
        #print(eqn)
        equationLabel = Label(self.win, text = self.eqn )
        equationLabel.grid(row=2,column=0, columnspan = 3)
        kickoffLabel = Label(self.win, text = "kickoff time:" )
        kickoffLabel.grid(row=3, column=0)    
        kickoffEntry = Entry(self.win, textvariable=self.kickVar)
        kickoffEntry.grid(row=3, column=1)
        opponentLabel = Label(self.win, text = "Opponent:" )
        opponentLabel.grid(row=4, column=0)   
        opponentEntry = Entry(self.win, textvariable=self.opponentVar)
        opponentEntry.grid(row=4, column=1)
        gwLabel = Label(self.win, text = "GW:" )
        gwLabel.grid(row=5, column=0)
        gwEntry = Entry(self.win, textvariable=self.gwVar)
        gwEntry.grid(row=5, column=1)
        calculateButton = Button(self.win, text= "Calculate", command = self.calculate_score)
        calculateButton.grid(row=6, column=1, columnspan=2)
        
        
    def calculate_score(self):
        kickoff = self.kickVar.get()
        opponent = self.opponentVar.get()
        gw = self.gwVar.get()
        print(kickoff)
        expected_points = self.kickoff_coeff*int(kickoff)+self.team_coeff*int(opponent)+self.gw_coeff*int(gw)+self.intercept
        pointsLabel = Label(self.win, text = str(expected_points))
        pointsLabel.grid(row=7, column =1, columnspan=3)
        
        
        
        
        
        
rootWin = Tk()
app = fpl_predictor(rootWin)
rootWin.mainloop()