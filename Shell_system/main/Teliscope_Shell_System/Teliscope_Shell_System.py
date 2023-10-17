from Backend_Functions import *
from datetime import datetime
from Astro_Calc_Functions import *
#import ImportFile

run = True              # variable to run main loop
validInput = False      # used to check for valid input
validBody = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"]
date_time = datetime.now()  # Current time 
CU_locat = [44.6636819, -74.997711, 143]     # Clarksons lat(degrees) lon(degrees) eli(m)


ser = Setup_Uart_port()        # Gets port and sets up codition

# Main loop
while(run):
    while validInput == False:
        print("a: Select angles or sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune for planets or end")
        target = input("Enter target: ")
        target = str(target)
        target.lower()

        if target in validBody:
            isPlanet = True
        else:
            isPlanet = False

        if(target == "a"):
            (x_ang, y_ang) = Get_User_angles()  # gets user information
            validInput = True   # breaks out of loop

        elif(isPlanet == True):    # if not found in planet list
            (x_ang, y_ang) = getAngles(target,date_time,CU_locat) # calculate angles check if area of operation 
            if (Input_Valid(0, 90, y_ang) == True and Input_Valid(0, 360, x_ang) == True):
                validInput = True   # breaks out of input loop
            else:
                print("Planet not in operational range") # informs user that planet not in poerational range 
                validInput = False   # Ensures that the new input is collected 
        elif(target == "end"):
            run = False # gets out of run loop
            validInput = True   # breaks out of loop
            y_ang = 0   # sets the system back to the origin
            x_ang = 0   # sets the system back to the origin
        else:
            print("Not valid input")    # Prints if the input isn't expected 

    if target != "end":
        validInput = False  # resets user choice
    
    x_data = angle_to_TX_data(x_ang) # Convert to data and send data through Uart
    y_data = angle_to_TX_data(y_ang) # Convert to data and send data through Uart

    Uart_Tx(ser, x_data, y_data) # sends data through uart

Close_Uart(ser)     # Terminates connection