#!/usr/bin/env python3
"""
Command Publisher Node - Reads parameters from turtle_param.yaml
and publishes TurtleCommand messages to /smart_turtle/command.
"""

import rclpy
from rclpy.node import Node
from smart_turtle_interface.msg import TurtleCommand


class CommandPublisher(Node):
    """
    Publisher node that reads pattern and speed parameters,
    loads them into a TurtleCommand message, and publishes
    to /smart_turtle/command every 1.0 second.
    """

    def __init__(self):
        super().__init__('command_publisher')

        # Declare parameters with defaults
        self.declare_parameter('command', 'circle')
        self.declare_parameter('speed', 1.0)

        # Create publisher on /smart_turtle/command topic
        self.publisher_ = self.create_publisher(
            TurtleCommand,
            '/smart_turtle/command',
            10
        )

        # Timer to publish every 1.0 second
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('Command Publisher Node has started.')

    def timer_callback(self):
        """Read parameters and publish TurtleCommand message."""
        # Get current parameter values (allows dynamic reconfiguration)
        command = self.get_parameter('command').get_parameter_value().string_value
        speed = self.get_parameter('speed').get_parameter_value().double_value

        # Create and populate the message
        msg = TurtleCommand()
        msg.command = command
        msg.speed = speed

        # Publish the message
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publishing: command="{msg.command}", speed={msg.speed}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CommandPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
