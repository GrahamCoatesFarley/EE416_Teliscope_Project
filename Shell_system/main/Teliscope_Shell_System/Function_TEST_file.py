from Astro_Calc_Functions import *
#from Frontend_Functions import *
from Backend_Functions import *
from datetime import datetime

date_time = datetime.now()
#print("Date and time: " + str(date_time))


CU_locat = [44.6636819, -74.997711, 143]     # Clarksons lat(degrees) lon(degrees) eli(m)
(x, y) = getAngles("Moon", date_time, CU_locat)

print("X position: " + str(x))
print("Y position: " + str(y))