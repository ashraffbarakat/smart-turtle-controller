import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')

        self.declare_parameter('safe_distance', 0.85)
        self.declare_parameter('linear_speed', 0.45)
        self.declare_parameter('angular_speed', 0.9)
        self.declare_parameter('front_angle_deg', 30.0)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self.turning_direction = 0.0  # 0 = moving straight, >0 = left, <0 = right
        self.get_logger().info('Obstacle Avoidance Node (Maze Edition) Started!')

    def get_sector_min(self, ranges, angle_min, angle_increment, start_deg, end_deg):
        min_dist = float('inf')
        for i, r in enumerate(ranges):
            if math.isinf(r) or math.isnan(r) or r <= 0.16:
                continue
            angle_deg = math.degrees(angle_min + i * angle_increment)
            while angle_deg > 180.0:
                angle_deg -= 360.0
            while angle_deg < -180.0:
                angle_deg += 360.0

            if start_deg <= angle_deg <= end_deg:
                if r < min_dist:
                    min_dist = r
        return min_dist

    def scan_callback(self, msg: LaserScan):
        safe_dist = self.get_parameter('safe_distance').value
        lin_speed = self.get_parameter('linear_speed').value
        ang_speed = self.get_parameter('angular_speed').value
        front_ang = self.get_parameter('front_angle_deg').value

        # Front cone [-30, 30], Wider side lookahead [30, 140] and [-140, -30] to spot U-turn exits
        front_min = self.get_sector_min(msg.ranges, msg.angle_min, msg.angle_increment, -front_ang, front_ang)
        left_min = self.get_sector_min(msg.ranges, msg.angle_min, msg.angle_increment, front_ang, 140.0)
        right_min = self.get_sector_min(msg.ranges, msg.angle_min, msg.angle_increment, -140.0, -front_ang)

        cmd = Twist()

        # Add hysteresis (+0.25m) so the robot finishes its turn cleanly before driving forward
        clear_threshold = safe_dist + 0.25 if self.turning_direction != 0.0 else safe_dist

        if front_min > clear_threshold:
            self.turning_direction = 0.0
            cmd.linear.x = lin_speed
            cmd.angular.z = 0.0
        else:
            cmd.linear.x = 0.0
            # Lock turning direction until front is clear so it completes 180-degree U-turns
            if self.turning_direction == 0.0:
                self.turning_direction = ang_speed if left_min >= right_min else -ang_speed
            cmd.angular.z = self.turning_direction

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()