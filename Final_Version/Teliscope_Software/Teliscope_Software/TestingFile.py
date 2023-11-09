import PySimpleGUI as GUI
from GUI_Functions import *
from AstroCalc import *
from BackEnd import *
from datetime import datetime
import tkinter as tk


yearMin = int(datetime.now().strftime("%Y"))- 3
yearMax = yearMin + 7
year = list(range(yearMin, yearMax))
print(year)



#GetPort(tk)
i=0
while True:
    i = i+1
    time = datetime.now()
    print("Time now: ", datetime.now())
    print("Time sec: ", datetime.now().strftime("%S"))
    
    if i == 5:
        break