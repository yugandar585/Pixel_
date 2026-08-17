#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("[pixel_beta] Waiting for Navigation2 to activate...")
    navigator.waitUntilNav2Active()
    print("[pixel_beta] Navigation2 is ready!")

    # Target Goal (x=2.0m, y=1.5m)
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 2.0
    goal_pose.pose.position.y = 1.5
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    print(f"[pixel_beta] Navigating to goal: x={goal_pose.pose.position.x}, y={goal_pose.pose.position.y}")
    navigator.goToPose(goal_pose)

    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(f"Distance remaining: {feedback.distance_remaining:.2f} meters")

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("[pixel_beta] Goal reached successfully!")
    elif result == TaskResult.CANCELED:
        print("[pixel_beta] Navigation canceled!")
    elif result == TaskResult.FAILED:
        print("[pixel_beta] Navigation failed!")

    rclpy.shutdown()

if __name__ == '__main__':
    main()