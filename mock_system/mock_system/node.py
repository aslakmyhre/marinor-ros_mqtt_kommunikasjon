import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool


class MockSystem(Node):
    """Mock System node that publishes battery and autonomous mode status."""

    def __init__(self):
        super().__init__('mock_system')
        self.battery_pub = self.create_publisher(Float32, '/system/battery', 10)
        self.autonomous_pub = self.create_publisher(Bool, '/system/autonomous', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.get_logger().info('Mock System node initialized')

    def publish_data(self):
        battery = Float32(data=85.5)
        autonomous = Bool(data=True)
        self.battery_pub.publish(battery)
        self.autonomous_pub.publish(autonomous)


def main(args=None):
    rclpy.init(args=args)
    node = MockSystem()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
