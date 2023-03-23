import logging as log
from datetime import datetime
from functools import partial
from time import sleep

from utils import createCubes, releaseCubes, Cube
from utils import PostureType, NotifyType, TargetPointAngleType, MovementType, MotorInfoType
from utils import DirectionType, SpeedPriorityType, AdditionalWriteSettingType

cubes = createCubes()

try:
    def listener(cube: Cube, notificationType: str, e):
        #log.debug("%s, %s, %s, %s", datetime.now().isoformat(), cube.name, notificationType, e)
        if e.type == MotorInfoType.SPEED:
            log.debug("motor speed notify %s %s", e.left, e.right)

    cube = cubes[0]
    cube.setConfigMotorSpeedNotify()
    cube.motor.addListener(partial(listener, cube, 'MotorNotify'))
    cube.motor.enableNotification()

    log.debug("forward")
    cube.setMotorWithAcceleration(50, 100)
    sleep(1)
    log.debug("backward")
    cube.setMotorWithAcceleration(50, 100, DirectionType.BACKWARD)
    sleep(2)
    log.debug("forward and turn")
    cube.setMotorWithAcceleration(50, 100, DirectionType.FORWARD, 45)
    sleep(2)
    log.debug("backward and turn")
    cube.setMotorWithAcceleration(50, 100, DirectionType.BACKWARD, 45, DirectionType.BACKWARD)
    sleep(2)
    cube.setMotor(0,0)

    while True:
        sleep(1)
        cube.setMotorWithAcceleration(50, 10, DirectionType.FORWARD, 45)

finally:
    releaseCubes(cubes)
