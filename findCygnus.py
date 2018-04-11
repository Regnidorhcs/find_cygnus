import math
import numpy as np
import datetime
from servosix import ServoSix
ss = ServoSix()

# a bunch of constants
vGalRot= 220
pi=np.pi
degs = 180.0/pi
rads = pi/180.0

# London UCL
LABLat= 51.525293
LABLong= -0.133674

now = datetime.datetime.utcnow()
year=now.year
month=now.month
day=now.day
hour=now.hour + now.minute/60.

def FNrange (x):
    b = x / 2./pi
    if round(b)-b<0 :
        a = 2.*pi * (b - round(b))
    else:
        a = 2.*pi * (b - round(b)-1)
    if a<0:
        while a<0:
         a+=2.*pi
        return a
    else:
        return a


#MJD
a = (14. - month) / 12.
y = year + 4800. - a
m = month + 12. * a - 3.
MJD = (day + (153. * m + 2.) / 5.  + 365. * y + y / 4. - y / 100. + y / 400. - 32045. ) - 2400000.5

if round(MJD)-MJD<0 :
    tnot = (round(MJD) - 55197.5 )/36525.0
else:
    tnot = (round(MJD)-1 - 55197.5 )/36525.0


luku = - 7. * (year + (month + 9.)/12.)/4. + 275.*month/9. + day + year*367.
FNday = luku - 730530.0 + hour/24.0



La=281.0298+36000.77*tnot+0.04107*hour
g=357.9258+35999.05*tnot+0.04107*hour
sunsEclLong2 = La+(1.915-0.0048*tnot)*np.sin(g*degs)+0.020*np.sin(2.*g*rads)

# print " sunsEclLong2 ", sunsEclLong2 //Correct

w = 282.9404 + 4.70935E-5 * FNday
M = 356.047 + 0.9856002585 * FNday
L = FNrange(w * rads + M * rads)

#TLab
GMST0 = L*degs/15.0 + 12.0
tlab = (GMST0 + hour + LABLong/15.0)*rads
#GECtoLAB
GECtoLAB = np.array([ [-np.sin(LABLat*rads)*np.cos(15.*tlab), -np.sin(LABLat*rads)*np.sin(15.*tlab) , np.cos(LABLat*rads)],[ np.sin(15.*tlab), -np.cos(15.*tlab),0.],[ np.cos(15.*tlab)*np.cos(LABLat*rads), np.cos(LABLat*rads)*np.sin(15.*tlab) ,np.sin(LABLat*rads)]])

#GALtoGEC
GALtoGEC=np.array([[-0.06699,0.4927 ,-0.8676], [-0.8728,-0.4503, -0.1884 ],[-0.4835, 0.7446, 0.4602]])

#GALtoLAB
GALtoLAB = GECtoLAB.dot(GALtoGEC)
#Setting up velocity vectors for celestial and terrestial objects (except from the sun).

#vel of sun precession
vSolMotGAL = [11.1,12.2,7.3]
#vel from galactic revolution

vGalRotGAL=[0.,vGalRot,0.]
#vel from revolution of earth


vErathIn=29.8*(1-0.016722*np.sin(sunsEclLong2-14.)*rads)
betax=-5.5303
betay=59.575
betaz=29.812
lamdax=266.141
lamday=-13.3485
lamdaz=179.3212

vEarthRevGAL= [vErathIn*np.cos(betax*rads)*np.sin((sunsEclLong2-lamdax)*rads), vErathIn*np.cos(betay*rads)*np.sin((sunsEclLong2-lamday)*rads) ,vErathIn*np.cos(betaz*rads)*np.sin((sunsEclLong2-lamdaz)*rads)]
vroteq= 0.465102

vEarthRotLAB=[0.,-vroteq*np.cos(LABLat*rads),0.]
cygnusLAB = GALtoLAB.dot(np.add(np.add(vGalRotGAL,vEarthRevGAL),vSolMotGAL)) + vEarthRotLAB
norm=np.linalg.norm(cygnusLAB)
cygnusLAB=cygnusLAB/norm

azim = math.atan2(cygnusLAB[1],cygnusLAB[0])
azim = FNrange(-azim)
altit = np.arcsin(cygnusLAB[2])

# print "time = ", year, month ,day ,hour
# print "azim ",azim
# print "altit ",altit


correction=0
position_servo1 =(pi-FNrange(azim+correction))*degs
position_servo2 =(2*pi-FNrange(azim+correction))*degs

if FNrange(azim+correction) < pi:
    ss.set_servo(2, altit*degs)
    ss.set_servo(1, position_servo1)
else:
    ss.set_servo(2, (pi-altit) * degs)
    ss.set_servo(1, position_servo2)

#print "pos_se1 ",position_servo1
#print "pos_se2",position_servo2