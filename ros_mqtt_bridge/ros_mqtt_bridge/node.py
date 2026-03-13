import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Float32, Bool
import paho.mqtt.client as mqtt
from dotenv import load_dotenv, find_dotenv
import os
import boat_pb2  # NEW: required for protobuf output


class RosMqttBridge(Node):
    """ROS2 → MQTT bridge that publishes protobuf Boat messages to mqtt_topic."""

    def __init__(self):
        super().__init__('ros_mqtt_bridge')

        # Load .env config
        load_dotenv(find_dotenv())
        mqtt_host = os.getenv("MQTT_HOST", "localhost")
        mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
        mqtt_username = os.getenv("MQTT_USERNAME")
        mqtt_password = os.getenv("MQTT_PASSWORD")
        self.mqtt_topic = os.getenv("MQTT_TOPIC", "marinor/boat/proto")

        # MQTT setup
        self.client = mqtt.Client()
        if mqtt_username:
            self.client.username_pw_set(mqtt_username, mqtt_password or "")

        try:
            self.client.connect(mqtt_host, mqtt_port, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            self.get_logger().error(f"MQTT connection failed: {e}")

        # Internal state: we build a complete Boat message
        self.boat_msg = boat_pb2.Boat()

        # Subscribe to ROS topics
        self.create_subscription(Point, "/gps/location", self._on_gps_location, 10)
        self.create_subscription(Float32, "/gps/heading", self._on_heading, 10)
        self.create_subscription(Float32, "/system/battery", self._on_battery, 10)

        self.get_logger().info("ROS MQTT Bridge initialized")


    # -----------------------------------
    # ROS Callbacks → update protobuf msg
    # -----------------------------------

    def _on_gps_location(self, msg: Point):
        self.boat_msg.position.latitude = msg.x
        self.boat_msg.position.longitude = msg.y
        self._publish_proto()

    def _on_heading(self, msg: Float32):
        self.boat_msg.direction = msg.data
        self._publish_proto()

    def _on_battery(self, msg: Float32):
        self.boat_msg.battery_percentage = msg.data
        self._publish_proto()

    # -----------------------------------
    # Publish final protobuf message
    # -----------------------------------

    def _publish_proto(self):
        """Serialize current Boat protobuf and send to mqtt_topic."""
        try:
            payload = self.boat_msg.SerializeToString()
            self.client.publish(self.mqtt_topic, payload)
        except Exception as e:
            self.get_logger().error(f"Failed to publish protobuf: {e}")

    # -----------------------------------
    # Shutdown
    # -----------------------------------

    def destroy_node(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RosMqttBridge()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()