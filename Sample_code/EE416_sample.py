from Functions import *                                                 # Imports functions from project function files 

serial = Setup_Uart_port()                                              # Sets up communication port

(H_Angle, V_Angle) = Get_User_angles()                                  # gets two angles from user

std_vect_len = 8                                                        # Number of bits in standard logic vector 
V_data = angle_to_TX_data(V_Angle)                                      # Calculates what the vertical motor data will be
H_data = angle_to_TX_data(H_Angle,)                                     # Calculates what the horizontal motor data will be


Uart_Tx(serial, H_data, V_data)                                         # sends data through Uart
Close_Uart(serial)                                                      # Closes Uart communication port

print("Program Complete")                                               # Completion message 