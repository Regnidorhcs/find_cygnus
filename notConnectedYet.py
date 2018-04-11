from servosix import ServoSix
import time


#
ss = ServoSix()
ss.set_servo(1,0)
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
