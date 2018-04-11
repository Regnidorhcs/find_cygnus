from servosix import ServoSix
import time
import numpy as np
import math
import FaBo9Axis_MPU9250
import time
import sys
import datetime
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

ss = ServoSix()
i=0
while i <2:

    for j in range (80,110):
        ss.set_servo(1,j)
        time.sleep(0.05)
    for j in range (80,110):
        ss.set_servo(1,180-j)
        time.sleep(0.05)
    
    i+=1