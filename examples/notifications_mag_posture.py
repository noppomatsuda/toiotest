import logging as log
from datetime import datetime
from functools import partial
from time import sleep

from utils import createCubes, releaseCubes, Cube
from utils import MagneticSenseType, PostureType, NotifyType

cubes = createCubes()

try:
    def listener(cube: Cube, notificationType: str, e):
        log.debug("%s, %s, %s, %s", datetime.now().isoformat(), cube.name, notificationType, e)

    for cube in cubes:
        cube.setConfigMagneticSensor(MagneticSenseType.FORCE, 0.5, NotifyType.CHANGED)
        cube.setConfigHighPrecisionTiltSensor(PostureType.EULER, 0.5, NotifyType.CHANGED)
        cube.motion.addListener(partial(listener, cube, 'MagAndPosture'))
        cube.motion.enableNotification()

    while True:
        sleep(1)

finally:
    releaseCubes(cubes)
