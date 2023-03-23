import logging as log

from time import sleep, time
from utils import createCubes, releaseCubes

# Identify each cube by the color and the sound signal,
# and report the battery level on the console.
cubes = createCubes()

try:
    # do what you want to do
    cube = cubes[0]
    cube.turnLeft(90)
    cube.turnRight(90)    
    cube.turnLeft(45)
    cube.turnLeft(45)
    cube.turnRight(45)    
    cube.turnRight(45)    
    cube.turnRight(360)    
    cube.Straight(10)    
    pass

finally:
    # Disconnect
    releaseCubes(cubes)
