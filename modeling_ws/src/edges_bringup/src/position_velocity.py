#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class PositionVelocityNode(Node):

    def __init__(self):
        super().__init__('position_velocity_node')

        self.subscription = self.create_subscription(
            Odometry,
            '/odometry',
            self.odom_callback,
            10
        )

    def odom_callback(self, msg):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        velocity = msg.twist.twist

        # Convert quaternion to yaw angle
        yaw=math.atan2(
            2.0*(orientation.w * orientation.z +
            orientation.x * orientation.y),
            1.0-2.0*(
            orientation.y ** 2 + orientation.z ** 2))

        yaw_deg = math.degrees(yaw)

        print(
            f"\rPosition: X={position.x:.3f} m, "
            f"Y={position.y:.3f} m | "
            f"Yaw={yaw_deg:.1f} deg | "
            f"Linear velocity={velocity.linear.x:.3f} m/s | "
            f"Angular velocity={velocity.angular.z:.3f} rad/s",
            end="",
            flush=True
        )


def main(args=None):
    rclpy.init(args=args)
    node = PositionVelocityNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nNode stopped.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
