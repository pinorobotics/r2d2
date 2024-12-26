**r2d2** (ros2dorna2) - set of ROS2 packages which provide support for [Dorna2 robotic arm](https://dorna.ai/).

NOTE: This is unofficial Dorna ROS2 package. For official Dorna software follow https://dorna.ai/

List of packages:

- [r2d2_urdf](https://github.com/pinorobotics/r2d2_urdf)
- [r2d2_moveit_config](https://github.com/pinorobotics/r2d2_moveit_config)
- [r2d2_servo](https://github.com/pinorobotics/r2d2_servo)

Testing was done with ROS2 Humble.

# Build

```
cd <ROS WORKSPACE>/src
git clone \
  https://github.com/pinorobotics/r2d2_urdf \
  https://github.com/pinorobotics/r2d2_moveit_config \
  https://github.com/pinorobotics/r2d2_servo
cd ..
colcon build
source install/setup.zsh
```

# Contacts

aeon_flux <aeon_flux@eclipso.ch>
