import logging as log
from datetime import datetime
from functools import partial
from time import sleep

from utils import createCubes, releaseCubes, Cube
from utils import PostureType, NotifyType, TargetPointAngleType, MovementType, MotorInfoType, Target
from tomotoio.navigator import Mat

mat = Mat()
mat_cx = int(mat.center.x)
mat_cy = int(mat.center.y)
# x, y, AngleType, deg  
goals = [Target(mat_cx, mat_cy, TargetPointAngleType.NO_ROTATION, 0),
            Target(mat_cx - 50, mat_cy -50, TargetPointAngleType.NO_ROTATION, 0), 
            Target(mat_cx - 50, mat_cy +50, TargetPointAngleType.NO_ROTATION, 0),
            Target(mat_cx + 50, mat_cy +50, TargetPointAngleType.NO_ROTATION, 0),
            Target(mat_cx + 50, mat_cy -50, TargetPointAngleType.NO_ROTATION, 0),
            Target(mat_cx - 50, mat_cy -50, TargetPointAngleType.NO_ROTATION, 0)]
index = 0

cubes = createCubes()

try:
    def listener(cube: Cube, notificationType: str, e):
        global index
        # log.debug("%s, %s, %s, %s", datetime.now().isoformat(), cube.name, notificationType, e)
        if e.type == MotorInfoType.WITH_MULTIPLE_TARGETS:
            log.debug("setMotorWithMultipleTargets %s result %s", e.id, e.result)
            # add next target position
            if index < len(goals):
                cube.setMotorWithMultipleTargets(index, [goals[index]], 30)
                log.debug("add next target position %s: %s, %s", index, goals[index].x, goals[index].y)
                index = index +1
            else:
                log.debug("core cube reached to final target.")

    cube = cubes[0]
    cube.motor.addListener(partial(listener, cube, 'MotorNotify'))
    cube.motor.enableNotification()

    # First, add 2 target positions
    cube.setMotorWithMultipleTargets(index, [goals[index]], 50)
    index = index +1
    cube.setMotorWithMultipleTargets(index, [goals[index]], 30)
    index = index +1

    while True:
        sleep(1)

finally:
    releaseCubes(cubes)
