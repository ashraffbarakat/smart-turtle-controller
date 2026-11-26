#!/usr/bin/env python3
"""
Reset Node - Periodically calls /reset and /clear services
on the turtlesim node every 10 seconds to reset the turtle
to the origin and clear drawn paths.
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty


class ResetNode(Node):
    """
    Client node that every 10 seconds sends service requests
    to /reset and /clear to reset the turtle's position and
    clear the drawn path.
    """

    def __init__(self):
        super().__init__('reset_node')

        # Create service clients
        self.reset_client = self.create_client(Empty, '/reset')
        self.clear_client = self.create_client(Empty, '/clear')

        # Timer to call services every 10 seconds
        self.timer = self.create_timer(10.0, self.timer_callback)

        self.get_logger().info('Reset Node has started. Resetting every 10 seconds.')

    def timer_callback(self):
        """Call /reset and /clear services."""
        self._call_reset()
        self._call_clear()

    def _call_reset(self):
        """Send request to /reset service."""
        if not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('/reset service not available.')
            return

        request = Empty.Request()
        future = self.reset_client.call_async(request)
        future.add_done_callback(self._reset_callback)

    def _reset_callback(self, future):
        """Handle /reset service response."""
        try:
            future.result()
            self.get_logger().info('Successfully called /reset service.')
        except Exception as e:
            self.get_logger().error(f'Failed to call /reset: {e}')

    def _call_clear(self):
        """Send request to /clear service."""
        if not self.clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('/clear service not available.')
            return

        request = Empty.Request()
        future = self.clear_client.call_async(request)
        future.add_done_callback(self._clear_callback)

    def _clear_callback(self, future):
        """Handle /clear service response."""
        try:
            future.result()
            self.get_logger().info('Successfully called /clear service.')
        except Exception as e:
            self.get_logger().error(f'Failed to call /clear: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ResetNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
