#
# Copyright 2024 pinorobotics
#
# Website: https://github.com/pinorobotics/r2d2_servo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import xacro

from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.descriptions import ParameterValue

from launch.actions import ExecuteProcess

def generate_launch_description():
  this_folder = FindPackageShare('r2d2')
  urdf_folder = FindPackageShare('r2d2_urdf')
  control_folder = FindPackageShare('r2d2_control')
  robot_description_content = Command([
          PathJoinSubstitution([FindExecutable(name="xacro")]),
          " ",
          PathJoinSubstitution([urdf_folder, "urdf", "Dorna2.urdf"]),
      ])
  robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}

  rviz_config_file = PathJoinSubstitution([this_folder, "rviz", "r2d2.rviz"])

  # Loading all MoveIt configs generated by Setup Assistant
  # xxxclean parathesis
  moveit_config = (
    MoveItConfigsBuilder("r2d2")
      .to_moveit_configs())

  move_group_configuration = {
    "publish_robot_description_semantic": True,
    "allow_trajectory_execution": True,
    # Note: Wrapping the following values is necessary so that the parameter value can be the empty string
    "capabilities": moveit_config.move_group_capabilities["capabilities"],
    "disable_capabilities": moveit_config.move_group_capabilities["disable_capabilities"],
    # Publish the planning scene of the physical robot so that rviz plugin can know actual robot
    "publish_planning_scene": True,
    "publish_geometry_updates": True,
    "publish_state_updates": True,
    "publish_transforms_updates": True,
    "monitor_dynamics": False,
  }

  return LaunchDescription([
      # robot_state_publisher
      Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
      ),
      Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]),
      # Run Java based r2d2_control controller
      # Make sure to build r2d2_control package by following instructions inside it
      # See r2d2_control documentation for all supported options
      ExecuteProcess(
        cmd=['java',
             '-jar', PathJoinSubstitution([control_folder, "libs", "r2d2_control.jar"]),
             '-moveItConfigPath=' + str(moveit_config.package_path),
             '-debug=true'],
        output='screen'),
      Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters= [
          moveit_config.to_dict(),
          move_group_configuration,
        ],
        #extra_debug_args=["--debug"],
        # Set the display variable, in case OpenGL code is used internally
        additional_env={"DISPLAY": os.environ.get("DISPLAY", "")},
      )
    ])
