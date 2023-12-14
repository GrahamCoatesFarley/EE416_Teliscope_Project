import PySimpleGUI as GUI
from GUI_Functions import *
from AstroCalc import *
from BackEnd import *
from datetime import datetime
import tkinter as tk

ser = Setup_Uart_port(tk)    

date_time = datetime.now()                                          # Current time 
CU_locat = [44.6636819, -74.997711, 143]   

# Getting planet postion
(x, y) = GetPlanetAngles("sun",date_time, CU_locat)
print("Suns Horizontal position: " + str(x))
print("Suns Vertical position: " + str(y))

Uart_Tx(ser, x, y)  
