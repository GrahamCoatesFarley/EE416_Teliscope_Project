from ctypes.wintypes import DOUBLE
import ctypes  # An included library with Python install.
import serial
import time
from datetime import datetime
from AstroCalc import *
from tkinter import simpledialog

# Checks if number is between targets. Returns Boolean
def Angle_Valid(minimum, maximum, data):
    if minimum <= float(data) <= maximum:               # Ckecks if input is valid 
        return True                                     # user input valid
    return False

# Error message box
def ErrorMbox(title, text):
    return ctypes.windll.user32.MessageBoxW(0, text, title, 0)


# fuction that gets two valid angles fron user and returns two floats 
# NOT USED when GUI is implemented 
def Get_User_angles(): 
    horz_angle = input("Enter Horizontial Angle: ")     # gets horizontial angle from user 

    input_valid = Angle_Valid(0, 360, horz_angle)       # checks if user input valid

    while(input_valid == False):                        # Trggers if invalid 
        print("Out of bounds ")                         # informs the user input invalid
        horz_angle = input("Enter Hozizontial Angle: ") # gets horizontial angle from user 

        input_valid = Angle_Valid(0, 360, horz_angle)   # checks if user input valid

    vert_angle = input("Enter vertical Angle: ")        # gets Vertical angle from user 
    input_valid = Angle_Valid(0, 90, vert_angle)        # checks if user input valid

    while(input_valid == False):                        # Trggers if invalid 
        print("Out of bounds ")                         # informs the user input invalid
        vert_angle = input("Enter Vertical Angle: ")    # gets horizontial angle from user 

        input_valid = Angle_Valid(0, 90, vert_angle)    # checks if user input valid

    return (float(horz_angle), float(vert_angle))       # Returns angles 

#OUT DATED FUNCTION
# Function to convert an angle to a motor data function angles as a float and resultion int 
#def angle_to_Motor_data(Angle, resolution, minimum, maximum):
#    step = (maximum-minimum)/resolution                 # Calculates what 1 degree will be interms of resolution
#    return int(Angle*step)                              # Converts the angle to motor data

# Function to convert an angle to a motor data function angles as a float and resultion int 
def angle_to_TX_data(Angle):                            
    int_Angle = int(Angle*100)                         # Multiples angle by 100 and cast to int
    byte_arr_size = 2                                  # Size of byte array used that will be sent by Uart
    return int_Angle.to_bytes(byte_arr_size, 'big')    # Converts interger to a byte array


# Get serial port
#def GetPort():
#	port = input("Input COM port: ")                    # Prompts user 
#	return port                                         # returns port

def GetPort(tk):
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    COMport = simpledialog.askstring(title="Get serial", prompt="Enter Comunication port:")

    return COMport

# TODO try and add away to ensure that the user sets up a com port
def Setup_Uart_port(tk):  
    
    port = GetPort(tk)                                    # Gets port information
    ser = serial.Serial(port, 115200, timeout= None)    # Sets up the serial COM
    print("Com port established")

    return ser                                          # Returns serial class


# Sends data through Uart 
def Uart_Tx(ser, x_ang, y_ang):
    H_data = angle_to_TX_data(x_ang)                # Convert to data and send data through Uart
    V_data = angle_to_TX_data(y_ang)                # Convert to data and send data through Uart

    ser.write(H_data)
    ser.write('h'.encode('ascii'))                  # Notifies Board that data sent is horizontial
    
    time.sleep(.005)                                # waits 5ms before sending Vertical data 
    
    ser.write(V_data)	                            # sends Vertical data
    ser.write('v'.encode('ascii'))                  # Notifies the hardware that vertial data was sent

# Function for closing Uart connection
def Close_Uart(serial):
    serial.close()                                      # Closes connection


def GetKeys(D):
    keys = []
    for key in D.keys():
        keys.append(key)

    return keys

def FixNullVal(dict, keys):
    for keys in dict:
        if dict[keys] == '':
            dict[keys] = 1
    if dict["Year"] == 1:
        dict["Year"] = int(datetime.now().strftime("%Y"))

    return dict

# Funtion user for data validation
# returns system presets and comand angles 
def Input_Validation(UserData, CU_GPS):

    # Establish default if no input provided 
    if UserData["Planet"] == '':
        UserData["Ang_active"] = True

    if UserData["Horizontial"] == '':
        UserData["Horizontial"] = 0

    if UserData["Vertical"] == '':
        UserData["Vertical"] = 0

    if UserData["LAT"] == '':
        UserData["LAT"] = 0

    if UserData["LON"] == '':
        UserData["LON"] = 0

    if UserData["ALT"] == '':
        UserData["ALT"] = 0

    if UserData["Month"] == '':
        UserData["Month"] = 1

    if UserData["Day"] == '':
        UserData["Day"] = 1

    if UserData["Year"] == '':
        UserData["Year"] = int(datetime.now().strftime("%Y"))

    if UserData["Hour"] == '':
        UserData["Hour"] = 1

    if UserData["Min"] == '':
        UserData["Min"] = 1

    if UserData["Sec"] == '':
        UserData["Sec"] = 1

    # Validates the GPS cordinate
    if UserData["CU_GPS_active"] ==  False:
        if Angle_Valid(-90,90, float(UserData["LAT"])) == False:
            ErrorMbox("Validation Failed", "Invalid Latitude")
            return (False, 0, 0)    # Validation failed

        if Angle_Valid(-180,180, float(UserData["LON"])) == False:
            ErrorMbox("Validation Failed", "Invalid Longitude")
            return (False, 0, 0)    # Validation failed

        if str(UserData["LON"]).isnumeric() == False:
            ErrorMbox("Validation Failed", "Invalid Altitude")
            return (False, 0, 0)    # Validation failed

        location = [float(UserData["LAT"]), float(UserData["LON"]), float(UserData["ALT"])]

    else:   # runs if user selects Clarkson's GPS
        location = CU_GPS   # Sets location to Clarksons Coordinates

    print("Location: " + str(location))

    # Validates the provided time
    if UserData["Current_time"] == False:   # makes sure that the time provided is correct 
        date_time = datetime.now()  # sets date_time to current time 

        date_time = date_time.replace(minute=UserData["Min"], hour=UserData["Hour"], second=UserData["Sec"], year=UserData["Year"], month=UserData["Month"], day=UserData["Day"])
    
    else:
        date_time = datetime.now()  # sets date_time to current time 

    print("Date and time: " + str(date_time))

    # Validation for user angles 
    if UserData["Ang_active"]:
        if str(UserData["Vertical"]).isnumeric() == False:
            # Display pop up saying invalid input
            ErrorMbox("Validation Failed", "Vertical angle is not a number")
            return (False, 0, 0)    # Validation failed

        if str(UserData["Horizontial"]).isnumeric() == False:
            # Display pop up saying invalid input
            ErrorMbox("Validation Failed", "Horizontial angle is not a number")
            return (False, 0, 0)    # Validation failed

        if Angle_Valid(0, 90, UserData["Vertical"]) == False:
            # Display pop up window saying vertical angle is false
            ErrorMbox("Validation Failed", "Vertical Angle not in operation range")
            return (False, 0, 0)    # Validation failed

        if Angle_Valid(0, 360, UserData["Horizontial"]) == False:
            # Display pop up window saying Horizontial angle is false
            ErrorMbox("Validation Failed", "Horizontial Angle not in operation range")
            return (False, 0, 0)    # Validation failed

        X_ang = float(UserData["Horizontial"])
        Y_ang = float(UserData["Vertical"])
    # Validate that planet is within the operation range
    else:
        # checks if planet is valid and returns angles 
        (valid, X_ang, Y_ang) = Planet_Valid(UserData["Planet"], date_time, location)
        if valid == False:
            return (False, 0, 0)

    return(True,  X_ang, Y_ang)

# Planet Validation
def Planet_Valid(planet, date_time, location):
    (X_ang, Y_ang) = GetPlanetAngles(planet, date_time, location)
    if Angle_Valid(0, 90, Y_ang) == False:
        # Display pop up window saying vertical angle is false
        ErrorMbox("Validation Failed", "Planet not in operation range")
        return (False, 0, 0)    # Validation failed

    if Angle_Valid(0, 360, X_ang) == False:
        # Display pop up window saying Horizontial angle is false
        ErrorMbox("Validation Failed", "Planet not in operation range")
        return (False, 0, 0)    # Validation failed

    return(True, X_ang, Y_ang)
