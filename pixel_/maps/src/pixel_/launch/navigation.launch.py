import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_pixel_beta = get_package_share_directory('pixel_beta')
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    slam_params_file = LaunchConfiguration(
        'slam_params_file',
        default=os.path.join(pkg_pixel_beta, 'config', 'slam_toolbox_params.yaml')
    )

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_slam_params_file = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(pkg_pixel_beta, 'config', 'slam_toolbox_params.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node'
    )

    start_async_slam_toolbox_node = Node(
        parameters=[
            slam_params_file,
            {'use_sim_time': use_sim_time}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_slam_params_file,
        start_async_slam_toolbox_node
    ])