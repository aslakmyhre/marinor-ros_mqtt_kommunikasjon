Quick run

1. Start an MQTT broker (e.g., mosquitto).
2. Source ROS 2 environment and install package dependencies:
   - pip install -e ros_mqtt_bridge (or ensure paho-mqtt and python-dotenv are installed)
3. Copy .env.example to .env and adjust MQTT settings.
4. Run mock nodes:
   - ros2 run mock_gps mock_gps
   - ros2 run mock_system mock_system
5. Run the bridge:
   - ros2 run ros_mqtt_bridge ros_mqtt_bridge
6. Observe MQTT messages:
   - mosquitto_sub -h localhost -t "marinor/#" -v

Notes
- This bridge is intentionally small and explicit. To replace mock nodes with real nodes, ensure topic names and message types match or adjust subscription topics in ros_mqtt_bridge/node.py.

Running with Docker (ROS 2 Humble on macOS Apple Silicon)

This repository includes a Dockerfile that builds an arm64 ROS 2 Humble image with the workspace and required Python packages (paho-mqtt, python-dotenv).

Build the image (prefer native Apple Silicon build):

  docker build --platform linux/arm64 -t ros_humble_bridge ..

If you prefer emulation (slower):

  docker build --platform linux/amd64 -t ros_humble_bridge ..

Run the container interactively and use the sourced environment inside:

  docker run --rm -it \
    -v "$(pwd)/..:/root/ws" \
    -e MQTT_HOST=host.docker.internal \
    ros_humble_bridge

Inside the container:

  # source ROS and workspace
  source /opt/ros/humble/setup.bash
  source /root/ws/install/setup.bash

  # run mock nodes (in separate shells)
  ros2 run mock_gps mock_gps
  ros2 run mock_system mock_system

  # run the bridge
  ros2 run ros_mqtt_bridge ros_mqtt_bridge

Networking notes
- To reach an MQTT broker running on the macOS host, use MQTT_HOST=host.docker.internal when running the container.
- Alternatively run an MQTT broker in Docker and connect containers on the same Docker network:

  docker network create ros-net
  docker run -d --network ros-net --name mosquitto -p 1883:1883 eclipse-mosquitto
  docker run --rm -it --network ros-net -e MQTT_HOST=mosquitto ros_humble_bridge

When to install Python libraries
- Python libraries are installed during the Docker image build (pip3 install in the Dockerfile). For development you can also pip install in a running container or use the setup.py install approach.

