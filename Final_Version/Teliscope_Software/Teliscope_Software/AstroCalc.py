#from curses import panel
#import astropy
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time

def GetPlanetAngles(planet, date_time, location):
    time = Time(date_time)
    #print("Time: " + str(time))

    locat = EarthLocation(lat=location[0]*u.deg, lon=-location[1]*u.deg, height=location[2]*u.m )
    utcoffset = -4*u.hour                                                                           # Eastern Daylight Time
    time = time - utcoffset

    target = get_body(str(planet).lower(), time, locat)
    #print(str(target))

    Xangle = target.ra.deg
    Yangle = target.dec.deg

    return(Xangle, Yangle)
