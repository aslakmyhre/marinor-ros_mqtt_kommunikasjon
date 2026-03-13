import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Float32


class MockGPS(Node):
    """Mock GPS node that publishes location and heading."""

    def __init__(self):
        super().__init__('mock_gps')
        self.location_pub = self.create_publisher(Point, '/gps/location', 10)
        self.heading_pub = self.create_publisher(Float32, '/gps/heading', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.get_logger().info('Mock GPS node initialized')

    def publish_data(self):
        location = Point(x=-10.4, y=63.44, z=0.0)  # longitude, latitude, altitude
        heading = Float32(data=45.0)
        self.location_pub.publish(location)
        self.heading_pub.publish(heading)


def main(args=None):
    rclpy.init(args=args)
    node = MockGPS()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
