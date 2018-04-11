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


mag = mpu9250.readMagnet()
mx = mag['x'] 
my = mag['y']
mz = mag['z'] 

azim = math.atan2(my,mx)
azim = FNrange(-azim)

print azim*degs


correction=0
position_servo1 =(pi+correction)*degs


#
ss = ServoSix()
ss.set_servo(1,position_servo1)
ss.set_servo(2,0)





# for j in range (1,181):
# 	ss.set_servo(1,j)
#         ss.set_servo(2,j)
# 	print j, "degrees"
# 	time.sleep(0.3)
# for i in range (1,181):
#         ss.set_servo(1,180-i)
#         ss.set_servo(2,180-i)
#         print i, "degrees"
#         time.sleep(0.3)


#Test range of motions
