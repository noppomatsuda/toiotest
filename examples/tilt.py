import logging as log
from datetime import datetime
from functools import partial
from time import sleep

from utils import createCubes, releaseCubes, Cube
from utils import MagneticSenseType, AngleType, NotifyType
from utils import TiltEuler

cubes = createCubes()

roll = 0
pitch = 0
yaw = 0

try:
    def listener(cube: Cube, notificationType: str, e):
#        log.debug("%s, %s, %s, %s", datetime.now().isoformat(), cube.name, notificationType, e)
        global roll, pitch, yaw
        if(type(e) is TiltEuler):
            roll = e.roll
            pitch  = e.pitch
            yaw  = e.yaw
#            log.debug("%s, %s, %s, %s", datetime.now().isoformat(), roll, pitch, yaw)

    cubes[0].motion.addListener(partial(listener, cubes[0], 'motiontilt'))
    cubes[0].motion.enableNotification()

#    cubes[0].setConfigMagneticSensor(MagneticSenseType.FORCE, 0.5, NotifyType.CHANGED)
    cubes[0].setConfigHighPrecisionTiltSensor(AngleType.EULER, 0.1, NotifyType.PERIODIC)
    prev_yaw = yaw
    while True:
        log.debug("%s, %s, %s", roll, pitch, yaw)
        spd = 0
        if(abs(pitch) > 10) :
            spd = 0 - pitch
        else:
            spd = 0
        spd_l = spd
        spd_r = spd
        if(abs(roll) > 10) :
            if(roll > 0):
                spd_r = spd_r / 2
            else :
                spd_l = spd_l / 2
                
        if((spd == 0)  and (abs(prev_yaw - yaw) > 13)):
            if((prev_yaw - yaw) > 0):
                spd_r = 20
                spd_l = -20
            else:
                spd_r = -20
                spd_l = 20

        cubes[1].setMotor(spd_l, spd_r)
        prev_yaw = yaw
        sleep(0.1)

finally:
    releaseCubes(cubes)
