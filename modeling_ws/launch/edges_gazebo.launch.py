from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    urdf_file = PathJoinSubstitution([
        FindPackageShare('edges_description'),
        'urdf',
        'edges_mobile_robot.xacro'
    ])

    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    start_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_spawn_model.launch.py'
            ])
        ),
        launch_arguments={
            'world': 'empty',
            'topic': '/robot_description',
            'entity_name': 'edges_robot'
        }.items()
    )

    return LaunchDescription([
        start_robot_state_publisher,
        start_gazebo,
        TimerAction(
            period=5.0,
            actions=[spawn_robot]
        )
    ])
