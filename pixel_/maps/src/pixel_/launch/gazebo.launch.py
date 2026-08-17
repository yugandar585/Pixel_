import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_pixel_beta = get_package_share_directory('pixel_beta')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    world_file = LaunchConfiguration('world', default=os.path.join(pkg_pixel_beta, 'worlds', 'empty.sdf'))
    urdf_file = os.path.join(pkg_pixel_beta, 'urdf', 'pixel_beta.urdf')

    robot_description = ParameterValue(Command(['xacro ', urdf_file]), value_type=str)

    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(pkg_pixel_beta, 'worlds', 'empty.sdf'),
        description='Full path to world model file to load'
    )

    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description
        }]
    )

    spawn_robot_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'pixel_beta',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.05'
        ],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(declare_world_cmd)
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_robot_cmd)

    return ld