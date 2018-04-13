from servosix import ServoSix
import time
import numpy as np
import math
import FaBo9Axis_MPU9250
import time
import sys
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

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


pi=np.pi
degs = 180.0/pi

#correction=0
#position_servo1 =(pi+correction)*degs

    
mx=0
my=0
averageN=0
while averageN<20:
    mag = mpu9250.readMagnet()
    mx += mag['x'] 
    my += mag['y']
    averageN+=1
    time.sleep(0.1)

if (mx>0 and my>0):
    north=math.atan(mx/my)
elif (mx>0 and my<0):
    north=pi/2.+math.atan(-my/mx)
elif (mx<0 and my<0):
    north=pi+math.atan(mx/my)
else:
    north=2.*pi-math.atan(-mx/my)
north=20.*pi/40.-north
correction=north


i=0
while i <2:


    altit=pi/4
    azim=0
    ss = ServoSix()

    position_servo1 =(pi-FNrange(azim+correction))*degs
    position_servo2 =(2*pi-FNrange(azim+correction))*degs

    if FNrange(azim+correction) < pi:
        ss.set_servo(2, altit*degs)
        ss.set_servo(1, position_servo1)
    else:
        ss.set_servo(2, (pi-altit) * degs)
        ss.set_servo(1, position_servo2)
    
    pointer=0
    while pointer <4:
	altit+=pi/16
        if FNrange(azim+correction) < pi:
            ss.set_servo(2, altit*degs)
        else:
            ss.set_servo(2, (pi-altit) * degs)
	time.sleep(0.5)
        pointer+=1
    pointer=0
    while pointer <4:
	altit-=pi/16
        if FNrange(azim+correction) < pi:
            ss.set_servo(2, altit*degs)
        else:
            ss.set_servo(2, (pi-altit) * degs)
	time.sleep(0.5)
        pointer+=1
    i+=1
