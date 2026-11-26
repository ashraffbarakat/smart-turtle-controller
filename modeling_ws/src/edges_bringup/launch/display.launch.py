from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    urdf_file = PathJoinSubstitution([
        FindPackageShare('edges_description'),
        'urdf',
        'edges.urdf'
    ])

    rviz_config_path = PathJoinSubstitution([
        FindPackageShare('edges_description'),
        'rviz',
        'edges_config.rviz'
    ])

    robot_description = Command(['xacro', ' ', urdf_file])

    start_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    start_joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    start_rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path]
    )

    ld = LaunchDescription()

    ld.add_action(start_robot_state_publisher)
    ld.add_action(start_joint_state_publisher)
    ld.add_action(start_rviz)

    return ld