#!/usr/bin/env python3
"""
Smart Turtle Launch File - Launches all system components:
  1. Turtlesim Node
  2. Command Publisher Node
  3. Turtle Controller Node
  4. Reset Node

Loads parameters from config/turtle_param.yaml.
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Get the path to the config file
    config = os.path.join(
        get_package_share_directory('smart_turtle_bringup'),
        'config',
        'turtle_param.yaml'
    )

    return LaunchDescription([
        # 1. Turtlesim Node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            output='screen',
        ),

        # 2. Command Publisher Node (with parameters from YAML)
        Node(
            package='smart_turtle_py',
            executable='command_publisher',
            name='command_publisher',
            output='screen',
            parameters=[config],
        ),

        # 3. Turtle Controller Node
        Node(
            package='smart_turtle_py',
            executable='turtle_controller',
            name='turtle_controller',
            output='screen',
        ),

        # 4. Reset Node
        Node(
            package='smart_turtle_py',
            executable='reset_node',
            name='reset_node',
            output='screen',
        ),
    ])
