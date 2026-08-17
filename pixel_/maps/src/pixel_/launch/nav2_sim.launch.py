import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_pixel_beta = get_package_share_directory('pixel_beta')

    world = LaunchConfiguration('world', default=os.path.join(pkg_pixel_beta, 'worlds', 'empty.sdf'))
    map_file = LaunchConfiguration('map', default=os.path.join(pkg_pixel_beta, 'maps', 'my_map.yaml'))
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(pkg_pixel_beta, 'worlds', 'empty.sdf'),
        description='Full path to world SDF file'
    )

    declare_map_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(pkg_pixel_beta, 'maps', 'my_map.yaml'),
        description='Full path to map YAML file'
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock'
    )

    # 1. Gazebo + Robot State Publisher + Spawn Entity
    gazebo_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_pixel_beta, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    # 2. Nav2 Stack + Localization + RViz
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_pixel_beta, 'launch', 'navigation.launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'use_sim_time': use_sim_time,
            'use_rviz': 'true'
        }.items()
    )

    ld = LaunchDescription()
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_map_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(gazebo_bringup)
    ld.add_action(nav2_bringup)

    return ld