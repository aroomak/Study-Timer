#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:46:42 2021

@author: aram
"""

import time
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import datetime
import csv 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("190x160")
  
# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("My Study Track Timer")
  
# Declaration of variables
hour=StringVar()
minute=StringVar()
second=StringVar()
comnt = StringVar()
  
# setting the default value as 0
hour.set("00")
minute.set("00")
second.set("00")
comnt.set("")
  
# Use of Entry class to take input from the user
hourEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=hour)
hourEntry.place(x=30,y=10)
  
minuteEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=minute)
minuteEntry.place(x=80,y=10)
  
secondEntry= Entry(root, width=3, font=("Arial",18,""), textvariable=second)
secondEntry.place(x=130,y=10)
#Comment Box
comntEntry= Entry(root, width=11, font=("Arial",18,""), textvariable=comnt)
comntEntry.place(x=25,y=85)


def date_time():
    now = datetime.datetime.now()
    #print (now.strftime("%Y-%m-%d %H:%M:%S"))
    #date
    c_date = now.strftime("%Y-%m-%d")
    #time
    c_time = now.strftime("%H:%M:%S")
    return c_date, c_time


def submit():
    try:
        # the input provided by the user is
        # stored in here :temp
        temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
        #temp_2 = int(hour.get())*60 + int(minute.get())
        saveTime()
                
    except:
        print("Please input the right value")
    while temp >-1:
         
        # divmod(firstvalue = temp//60, secondvalue = temp%60)
        mins,secs = divmod(temp,60) 
  
        # Converting the input entered in mins or secs to hours,
        # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
        # 50min: 0sec)
        hours=0
        if mins >60:
             
            # divmod(firstvalue = temp//60, secondvalue 
            # = temp%60)
            hours, mins = divmod(mins, 60)
         
        # using format () method to store the value up to 
        # two decimal places
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
  
        # updating the GUI window after decrementing the
        # temp value every time
        root.update()
        time.sleep(1)
  
        # when temp value = 0; then a messagebox pop's up
        # with a message:"Time's up"
        if (temp == 0):
            #saveTime()
            messagebox.showinfo("Time Countdown", "Time's up ")
  
        # after every one sec the value of temp will be decremented
        # by one
        temp -= 1


def saveTime():
    temp_2 = int(hour.get())*60 + int(minute.get())
    
    # data to be written row-wise in csv fil 
    c_dt , c_tm = date_time()
    data = [[c_dt , c_tm, temp_2, (comnt.get())]] 

    # opening the csv file in 'a+' mode 
    file = open(r'/home/aram/Desktop/ReadingDB.csv', 'a+', newline ='') 
      
    # writing the data into the file 
    with file:     
        write = csv.writer(file) 
        write.writerows(data)
    return data

#Reading the DB
db_path= '/home/aram/Desktop/ReadingDB.csv'

db = pd.read_csv(db_path)

def sum_last_day():
    db['Date'] = pd.to_datetime(db['Date'], format='%Y-%m-%d').dt.date
    last_day = max(db.Date)
    last_day_sum = db.loc[db['Date'] == last_day, ['Length']].sum(axis=0)
    #df.loc[(df['age'] == 21) & df['favorite_color'].isin(array)]
    #last_day_1 = last_day -1
    message2 = ("On %s you studied %d minutes" %(str(last_day), int(last_day_sum)))
    messagebox.showinfo("Last Day", message2)
    #return (last_day_sum) #, last_day_1)

#s1

def DaySum(gday):
    day_sum = db.loc[db['Date'] == gday, ['Length']].sum(axis=0)
    return day_sum

def SubjectSum(comnt):
    subject_sum = db.loc[db['Comment'] == comnt, ['Length']].sum(axis=0)
    return subject_sum

listOfDayes = db.Date.unique()
hoursPerDay = []
for i in listOfDayes:
    hoursPerDay = np.append(hoursPerDay, DaySum(i))
    
listOfSubjects = db.Comment.unique()
hoursPerSubj = []
for i in listOfSubjects:
    hoursPerSubj = np.append(hoursPerSubj, SubjectSum(i))
    

def plotdays():
    #plotting
    #color_list = ['b', 'g', 'r']
    plt.bar(listOfDayes, hoursPerDay, color=['b','r'])
    y_pos = range(len(listOfDayes))
    plt.xticks(y_pos, listOfDayes, rotation=90)
    plt.show()
    
    
def plotSubjects():
    plt.bar(listOfSubjects, hoursPerSubj, color=['g','c'])
    y_pos = range(len(listOfSubjects))
    plt.xticks(y_pos, listOfSubjects, rotation=90)
    plt.show()
#e1


##Start Button
btn = Button(root, text='Start Timer', bd='5', command= submit)
btn.place(x = 40, y = 46)

##Aux_Bottuns
"""#Bottun1
btn = Button(root, text='Last Day', bd='4', command= sum_last_day)
btn.place(x = 120, y = 95)
"""
#Bottun2
btn = Button(root, text='Studies', bd='4', command= plotdays)
btn.place(x = 100, y = 120)

#Bottun3
btn = Button(root, text='Subjects', bd='4', command= plotSubjects)
btn.place(x = 5, y = 120)

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.iconphoto(False, tk.PhotoImage(file='/home/aram/Desktop/Dropbox/PythonTimer/timer.png'))
root.mainloop()
