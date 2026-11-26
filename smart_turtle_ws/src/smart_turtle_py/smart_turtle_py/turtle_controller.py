#!/usr/bin/env python3
"""
Turtle Controller Node - Subscribes to /smart_turtle/command,
interprets the pattern and speed, and publishes Twist commands
to /turtle1/cmd_vel to control the turtle's motion.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from smart_turtle_interface.msg import TurtleCommand
import math


class TurtleController(Node):
    """
    Subscriber node that receives TurtleCommand messages and
    generates appropriate Twist velocity commands based on the
    motion pattern (circle, spiral, square).
    """

    def __init__(self):
        super().__init__('turtle_controller')

        # Subscriber to /smart_turtle/command
        self.subscription = self.create_subscription(
            TurtleCommand,
            '/smart_turtle/command',
            self.command_callback,
            10
        )

        # Publisher to /turtle1/cmd_vel
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # State variables for patterns
        self.spiral_radius = 0.0  # For spiral pattern (increasing radius)
        self.square_state = 0  # State machine for square (0=forward, 1=turn)
        self.square_count = 0  # Counter for square timing
        self.square_side_length = 20  # Number of ticks per side
        self.square_turn_length = 8  # Number of ticks per turn

        self.get_logger().info('Turtle Controller Node has started.')

    def command_callback(self, msg):
        """Process received TurtleCommand and publish Twist."""
        pattern = msg.command.lower()
        speed = msg.speed

        twist = Twist()

        if pattern == 'circle':
            twist = self._circle(speed)
        elif pattern == 'spiral':
            twist = self._spiral(speed)
        elif pattern == 'square':
            twist = self._square(speed)
        else:
            self.get_logger().warn(f'Unknown pattern: "{pattern}". Stopping.')
            # twist remains all zeros (stop)

        self.velocity_publisher.publish(twist)
        self.get_logger().info(
            f'Pattern: {pattern} | linear.x={twist.linear.x:.2f}, '
            f'angular.z={twist.angular.z:.2f}'
        )

    def _circle(self, speed):
        """Generate Twist for circular motion."""
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = speed
        return twist

    def _spiral(self, speed):
        """Generate Twist for spiral motion (increasing radius)."""
        twist = Twist()
        self.spiral_radius += 0.05
        twist.linear.x = speed + self.spiral_radius
        twist.angular.z = speed
        return twist

    def _square(self, speed):
        """Generate Twist for square motion using a simple state machine."""
        twist = Twist()

        if self.square_state == 0:
            # Moving forward
            twist.linear.x = speed
            twist.angular.z = 0.0
            self.square_count += 1
            if self.square_count >= self.square_side_length:
                self.square_count = 0
                self.square_state = 1
        elif self.square_state == 1:
            # Turning 90 degrees
            twist.linear.x = 0.0
            twist.angular.z = math.pi / 2.0
            self.square_count += 1
            if self.square_count >= self.square_turn_length:
                self.square_count = 0
                self.square_state = 0

        return twist

    def reset_state(self):
        """Reset pattern state variables (called on /reset)."""
        self.spiral_radius = 0.0
        self.square_state = 0
        self.square_count = 0


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
