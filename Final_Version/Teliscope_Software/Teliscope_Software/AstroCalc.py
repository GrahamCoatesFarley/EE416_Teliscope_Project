#from curses import panel
#import astropy
from pickle import NONE
from pydoc import locate
from tkinter import UNITS
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body
#from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time

def GetPlanetAngles(planet, date_time, location):
    #solar_system_ephemeris.set('jpl')  

    time = Time(date_time)
    #print("Time: " + str(time))

    #locat = EarthLocation(lat=location[0]*u.deg, lon=location[1]*u.deg, height=location[2]*u.m )
    #locat = EarthLocation(lat=location[0], lon=location[1], height=location[2] )
    locat = EarthLocation(lat=location[0]*u.deg, lon=location[1]*u.deg, height=location[2]*u.m )

    utcoffset = -4*u.hour                       # Eastern Daylight Time
    time = time - utcoffset                     # Changes time to EST

    frame = AltAz(obstime=time, location=locat) # Adjusts refeence frame to altitude azimuth
    
    #target = get_body(body = str(planet).lower(), time = time, location = locat)
    target = get_body(body = str(planet).lower(), time = time)  # Gets target angles

    target_frame = target.transform_to(frame)                   # Adjuest the target to our frame
    #print("Target Fame: " + str(target_frame))

    Xangle = target_frame.az.deg        # Gets azimuth in degrees
    Yangle = target_frame.alt.deg       # Gets elivation in degrees


    return(Xangle, Yangle)