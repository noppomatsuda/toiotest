import logging as log
from datetime import datetime
from functools import partial
from time import sleep

from utils import createCubes, releaseCubes, Cube
from utils import PostureType, NotifyType, TargetPointAngleType, MovementType, MotorInfoType
from tomotoio.navigator import Mat

mat = Mat()
cubes = createCubes()

try:
    def listener(cube: Cube, notificationType: str, e):
        #log.debug("%s, %s, %s, %s", datetime.now().isoformat(), cube.name, notificationType, e)
        if e.type ==  MotorInfoType.WITH_TARGET:
            log.debug("setMotorWithTarget %s result %s", e.id, e.result)
        elif e.type == MotorInfoType.WITH_MULTIPLE_TARGETS:
            log.debug("setMotorWithMultipleTargets %s result %s", e.id, e.result)
        elif e.type == MotorInfoType.SPEED:
            log.debug("motor speed notify %s %s", e.left, e.right)


    cube = cubes[0]
    cube.setConfigMotorSpeedNotify()
    cube.motor.addListener(partial(listener, cube, 'MotorNotify'))
    cube.motor.enableNotification()

    mat_cx = int(mat.center.x)
    mat_cy = int(mat.center.y)
    cube.setMotorWithTarget(0, mat_cx, mat_cy, 50)
    sleep(3)
    # x, y, AngleType, deg  
    goals = [(mat_cx - 100, mat_cy -100, TargetPointAngleType.ABSOLUTE, 0), 
             (mat_cx - 100, mat_cy +100, TargetPointAngleType.ABSOLUTE, 90)]

    cube.setMotorWithMultipleTargets(1, goals, 30)
    while True:
        sleep(1)

finally:
    releaseCubes(cubes)
