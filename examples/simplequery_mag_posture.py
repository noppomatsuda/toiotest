import logging as log
from time import sleep

from utils import createCubes, releaseCubes
from utils import MagneticSenseType, PostureType, NotifyType
from utils import TiltEuler

# Identify each cube by the color and the sound signal,
# and report the battery level on the console.
cubes = createCubes(initialReport=True)

try:
    for i, c in enumerate(cubes):
        c.setConfigMagneticSensor(MagneticSenseType.FORCE, 0.1, NotifyType.PERIODIC)
        c.setConfigHighPrecisionTiltSensor(PostureType.EULER, 0.1, NotifyType.PERIODIC)
    for k in range(10):
        for i, c in enumerate(cubes):
            log.info("Cube #%d, Iteration #%d" % (i + 1, k + 1))
            log.info(c.motion.get())
        sleep(0.5)

finally:
    # Disconnect
    releaseCubes(cubes)
