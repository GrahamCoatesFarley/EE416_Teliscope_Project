from Angle_Class import *

import serial
import time


# Checks if number is between targets. Returns Boolean
def Input_Valid(minimum, maximum, data):
    if minimum <= float(data) <= maximum:               # Ckecks if input is valid 
        return True                                     # user input valid
    return False


# fuction that gets two valid angles fron user and returns two floats 
def Get_User_angles(): 
    horz_angle = input("Enter Horizontial Angle: ")     # gets horizontial angle from user 

    input_valid = Input_Valid(0, 360, horz_angle)       # checks if user input valid

    while(input_valid == False):                        # Trggers if invalid 
        print("Out of bounds ")                         # informs the user input invalid
        horz_angle = input("Enter Hozizontial Angle: ") # gets horizontial angle from user 

        input_valid = Input_Valid(0, 360, horz_angle)   # checks if user input valid

    vert_angle = input("Enter vertical Angle: ")        # gets Vertical angle from user 
    input_valid = Input_Valid(0, 90, vert_angle)        # checks if user input valid

    while(input_valid == False):                        # Trggers if invalid 
        print("Out of bounds ")                         # informs the user input invalid
        vert_angle = input("Enter Vertical Angle: ")    # gets horizontial angle from user 

        input_valid = Input_Valid(0, 90, vert_angle)    # checks if user input valid

    return (float(horz_angle), float(vert_angle))       # Returns angles 

#OUT DATED FUNCTION
# Function to convert an angle to a motor data function angles as a float and resultion int 
#def angle_to_Motor_data(Angle, resolution, minimum, maximum):
#    step = (maximum-minimum)/resolution                 # Calculates what 1 degree will be interms of resolution
#    return int(Angle*step)                              # Converts the angle to motor data

# Function to convert an angle to a motor data function angles as a float and resultion int 
def angle_to_TX_data(Angle):                            
    int_Angle = int(Angle*1000)                         # Multiples angle by 1000 and cast to int
    byte_arr_size = 19                                  # Size of byte array used that will be sent by Uart
    return int_Angle.to_bytes(byte_arr_size, 'big')     # Converts interger to a byte array


# Get serial port
def GetPort():
	port = input("Input COM port: ")                    # Prompts user 
	return port                                         # returns port


def Setup_Uart_port():  
    port = GetPort()                                    # Gets port information
    ser = serial.Serial(port, 115200, timeout= None)    # Sets up the serial com 
    return ser                                          # Returns serial class


# Sends data through Uart 
def Uart_Tx(ser, H_data, V_data):
    #ser.write(H_data.to_bytes(1, "big"))	            # sends Horizontial data
    ser.write(H_data)	            # sends Horizontial data

    time.sleep(.005)                                    # waits before sending Vertical data 
    #ser.write(V_data.to_bytes(1, "big"))	            # sends Vertical data
    ser.write(V_data)	            # sends Vertical data

# Function for closing Uart connection
def Close_Uart(serial):
    serial.close()                                      # Closes connection