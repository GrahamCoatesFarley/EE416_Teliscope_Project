# Imports
import PySimpleGUI as GUI
from GUI_Functions import *
from AstroCalc import *
from BackEnd import *
from datetime import datetime
import tkinter as tk
import time

Run_system = True                               # Run Varbible

# Lits of selectible celcial objects
PlanetList = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"]
date_time = datetime.now()                                          # Current time 
CU_locat = [44.6636819, -74.997711, 143]                            # Clarksons lat(degrees) lon(degrees) eli(m)
ValidInput = False                                                  # Variable used set detmine if user input is valid
Track = False                                                       # Variable for tracking enable 

# Window Configure
layout = GenerateLayout(GUI, PlanetList)                            # Generates the layout for the GUI window
GUI.theme('Dark2')                                             # Sets the theme for the GUI
margins = [200, 200]                                                # Screen margins 
window = CreateWindow(GUI, "Telescope Software", layout, margins)   # Creates window objects from layout

ser = Setup_Uart_port(tk)                                          # Gets port and establishes a connection

while Run_system:
    event, values = window.read(timeout=0)                          # reads in values and events from the window object; timeout equals zero is so the system is stuck waiting for an event
    #print(values)

    if event == "Terminate Program" or event == GUI.WIN_CLOSED:     # End program if user closes window or
        Run_system = False                                          # Breaks out of main loop
        #print("Program Ended")

    if (event == "Enter") or ((datetime.now().strftime("%S") == "00") and Track):                                            # User is finished with input 
        #print(values)  # print values of user input from GUI [Used for debugging]
        (ValidInput, X_ang, Y_ang) = Input_Validation(values, CU_locat)    # Passes user input for validation and returns variables 
        #print("Azimuth: " + str(X_ang))
        #print("Elivation: " + str(Y_ang))

        window['Horz_Dis'].update('Azimuth: ' + str(X_ang))         # Updates GUI Azimth angle
        window['Vert_Dis'].update('Elivation: ' + str(Y_ang))       # Updates GUI Elivation angle 

        if ValidInput:
            Uart_Tx(ser, X_ang, Y_ang)         # Transmits data through Uart
            #print("Data transmitted")
            time.sleep(1)                       # Waits one second to prevent track from catching and exicute multiple times

            if values["Ang_active"] == False:   # Check is tracking enabled 
                Track = True                    # Enable Tracking

        else:
            Track = False                       # Stops tracking 

        window['Track_Dis'].update('Tracking Active: ' + str(Track))        # Updates the window with tracking conditions

    if(event == 'Cancel Tracking'):
        Track = False                           # Stops tracking 

    if(event == 'Start Tracking'):
        if values['Ang_active'] == False and values['Current_time'] == True:       # Makes sure a planet is selected
            Track = True                        # Starts tracking 

        else:
            Track = False 
            ErrorMbox("Tracking Error","You have chosen settings that prevent tracking please chose a planet and current date and time")


window.close()          # Closed the window of the GUI
Uart_Tx(ser, 0, 0)     # Returns the teliscpe to the origin
Close_Uart(ser)        # Terminates Uart connection