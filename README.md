**This project is forked from https://github.com/kenichi884/tomotoio**

# Description

My test project playing with Sony Toio. See https://www.sony.net/SonyInfo/design/stories/toio/.

This runs on Linux with Python 3.6 or later. I am personally running this on Raspberry Pi 4 + Stretch.

Modified features from original tomotoio/tomotoio
* support toio core cube system software v02.0005 / BLE protocol v2.3.0
* Motor control with target specified
* Motor control with multiple targets specified
* Motor contorl with acceleration specified
* Posture angle detection
* Magnetic sensor
* Identification sensor notification frequency settings
* Shake detection
* motor speed information 

# Getting Started

1. Install the package with `pip`. If you want to just try, `pip install -e .` at the root directory will be convenient.
2. Power on your Toio cubes, and run `./scan-cubes.sh`. It will scan the cubes and create `toio-cubes.txt` that includes their MAC addresses. Note that the scanning requires the root privilege and you may be asked the `sudo` password.
3. Run examples, e.g. `python examples/soccer.py`.
  * Stay in the same directory as `toio-cubes.txt`.
  * The Toio collection mat is required.

# Examples (under examples directory)

* simple.py: Just connects to cubes, identifies themselves with sounds and lights, then disconnects
* soundeffects.py: Beep the sound effects from #0 to #10
* notifications.py: Outputs the notifications (positions, button states, motions) to the console.
* rotate.py: Cube #1 rotates to the direction of cube #2
* symmetric.py: Cube #1 moves to the point-symmetric position of cube #2
* circle.py: Cube #1 moves circularly assuming cube #2 as the center
* gravity.py: Cube #1 and #2 moves around the mat with a gravity (and repulsion if they are too close) between each other
* soccer.py: Cube #1 plays soccer using cube #2 as the ball (https://youtu.be/YhW3jLB9C4E)
* funmouse.py: Cube #1 works as a mouse, but be careful as it moves when you don't want! (https://youtu.be/EzOJ5VRSIUI)
* motor_with_target.py: Cube #1 moves to target position.
* motor_with_multiple_targets.py: Cube #1 moves to multiple target position.
* motor_with_acceleation.py: Cube #1 moves with acceleration change.
* notifications_mag_posture.py: Outputs the notifications (magnetic sensor and posture) to the console.
* tilt.py: Control Cube #2 by tilting Cube #1.
