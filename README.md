**r2d2** (ros2dorna2) - set of ROS2 packages which provide support for [Dorna2 robotic arm](https://dorna.ai/).

NOTE: This is unofficial Dorna ROS2 package. For official Dorna software follow https://dorna.ai/

List of packages:

- [r2d2_urdf](https://github.com/pinorobotics/r2d2_urdf)
- [r2d2_moveit_config](https://github.com/pinorobotics/r2d2_moveit_config)
- [r2d2_servo](https://github.com/pinorobotics/r2d2_servo)
- [r2d2_control](https://github.com/pinorobotics/r2d2_control)

Testing was done with ROS2 Humble.

# Build

Clone:
```
cd <ROS WORKSPACE>/src
git clone \
  https://github.com/pinorobotics/r2d2 \
  https://github.com/pinorobotics/r2d2_urdf \
  https://github.com/pinorobotics/r2d2_moveit_config \
  https://github.com/pinorobotics/r2d2_servo \
  https://github.com/pinorobotics/r2d2_control
```

Build Dorna2 controller:
```
cd r2d2_control
gradle clean build
```

Build ROS packages:
```
cd <ROS WORKSPACE>
colcon build
source install/setup.zsh
```

# Usage

Following command starts r2d2_control, MoveIt and RViz:
```
ros2 launch r2d2 r2d2_launch.py
```
It expects Dorna2 arm "Command Server" to be reachable on default URL (see `r2d2_control` package instructions how to redefine it).

After all nodes are started it is possible to Plan and Execute trajectories from MotionPlanning panel.

Other usage commands for **r2d2** packages can be found inside README files of the respective packages (r2d2_servo, r2d2_urdf, ...).

# Troubleshooting

## start point deviates from current robot state

Plan command inside RViz (MotionPlanning panel) could fail with the following error:
```
[move_group-3] Invalid Trajectory: start point deviates from current robot state more than 0.01 [move_group-3] joint 'Joint_0': expected: 3.01878, current: -0.0814851  
```

This happens because RViz seems to cache last "current" state and does not update it after Execute command.
To fix this, select "current" state again inside "Start State" drop down.

# Contacts

aeon_flux <aeon_flux@eclipso.ch>
