import rclpy
from rclpy.node import Node


class RosMqttBridge(Node):
    """Minimal ROS 2 MQTT Bridge node."""

    def __init__(self):
        super().__init__('ros_mqtt_bridge')
        self.get_logger().info('ROS MQTT Bridge node initialized')


def main(args=None):
    rclpy.init(args=args)
    node = RosMqttBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
