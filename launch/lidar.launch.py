from launch import LaunchDescription
from launch_ros.actions import Node
import launch 
import launch_ros.actions
from launch.substitutions import Command, LaunchConfiguration
import os 
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(package='lidar_scan').find('lidar_scan')
    #default_rviz_config_path = os.path.join(pkg_share, 'rviz/wamv_config.rviz')
    
    lidar_pub = Node(
            package='lidar_scan',
            executable='lidar_pub'
    )
    lidar0_frame=Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['--x', '0.25', '--y', '0', '--z', '0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base_link', '--child-frame-id', 'lidar_0']
    )
    test_frame=Node( 
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['--x', '3', '--y', '0', '--z', '5', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'zed_2i_base_link', '--child-frame-id', 'test2']
    )
    zed_left_frame=Node( 
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['--x', '5', '--y', '0', '--z', '5', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'zed2i_base_link', '--child-frame-id', 'zed2i_right_camera_optical_frame']
    )
    base_footprint=Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['--x', '0', '--y', '0', '--z', '2', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'lidar_0', '--child-frame-id', 'base_footprint']
    )
    pcl2_ls=Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pcl_to_laserscan',
            output='screen',
            parameters=[
                {
                    'target_frame': 'lidar_0',  # Replace 'base_link' with your target frame
                    'transform_tolerance': 0.01,   # Adjust the transform tolerance as needed
                }
            ],
            remappings=[
                #('/cloud_in', '/rgb_pointcloud'),
                ('/cloud_in', '/lidar_0/m1600/pcl2'),  # Replace with your PointCloud2 topic
                ('/scan', '/scan'),        # Replace with the desired LaserScan topic
            ],
        )
 
    
    colorMappingNode = Node(
            package='lidar_scan',
            executable='colorMappingNode'
    )
    fixed_math_node = Node(
        package='lidar_scan',
        executable='fixed_math'
    )
    map_node=Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['--x', '0', '--y', '0', '--z', '2', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base_footprint', '--child-frame-id', 'map']
    )
    odom_node=Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['--x', '0', '--y', '0', '--z', '1', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'map', '--child-frame-id', 'odom']
    )


    return LaunchDescription([
        #launch_ros.actions.SetParameter(name='use_sim_time', value=True), # attempt to solve TF_OLD_DATA error

        launch.actions.DeclareLaunchArgument('map_topic', default_value='/map',
                                            description='Occupancy grid map topic'),
        lidar0_frame,
        base_footprint,
        pcl2_ls,
        colorMappingNode
        #fixed_math_node
        #rviz_node
        #rviz_node
        #map_ned,
        #test_frame,
        #zed_left_frame,
    ])