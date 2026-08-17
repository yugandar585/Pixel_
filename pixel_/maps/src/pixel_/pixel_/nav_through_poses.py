#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def create_pose(navigator, x, y, yaw=0.0):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.position.z = 0.0
    pose.pose.orientation.w = 1.0
    return pose

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("[pixel_beta] Waiting for Navigation2 to activate...")
    navigator.waitUntilNav2Active()
    print("[pixel_beta] Navigation2 active. Starting patrol...")

    # Multi-point patrol route
    waypoints = [
        create_pose(navigator, 2.0, 0.0),
        create_pose(navigator, 2.0, 2.0),
        create_pose(navigator, 0.0, 2.0),
        create_pose(navigator, 0.0, 0.0)
    ]

    navigator.goThroughPoses(waypoints)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            print(f"Remaining waypoints: {feedback.number_of_poses_remaining}")

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("[pixel_beta] Finished patrol route!")
    else:
        print(f"[pixel_beta] Patrol ended with status: {result}")

    rclpy.shutdown()

if __name__ == '__main__':
    main()