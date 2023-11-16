import PySimpleGUI as GUI
from GUI_Functions import *
from AstroCalc import *
from BackEnd import *
from datetime import datetime
import tkinter as tk

date_time = datetime.now()                                          # Current time 
CU_locat = [44.6636819, -74.997711, 143]   

# Getting planets postion
(x, y) = GetPlanetAngles("sun",date_time, CU_locat)
print("Suns Horizontial postition: " + str(x))
print("Suns Vertical postition: " + str(y))
