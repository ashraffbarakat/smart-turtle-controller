from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('edges_description'),
                'launch',
                'edges_gazebo.launch.py'
            ])
        )
    )

    rviz_config = PathJoinSubstitution([
        FindPackageShare('edges_description'),
        'rviz',
        'edges_config.rviz'
    ])

    avoidance_config = PathJoinSubstitution([
        FindPackageShare('obstacle_avoidance_controller'),
        'config',
        'obstacle_avoidance.yaml'
    ])

    start_rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    start_avoidance = Node(
        package='obstacle_avoidance_controller',
        executable='obstacle_avoidance_node',
        parameters=[avoidance_config, {'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gazebo_sim,
        start_rviz,
        TimerAction(period=5.0, actions=[start_avoidance]),
    ])
