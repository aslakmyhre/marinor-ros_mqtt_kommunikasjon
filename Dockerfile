FROM --platform=linux/arm64 osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

# Minimal build tools and colcon
RUN apt-get update && apt-get install -y \
    python3-pip python3-colcon-common-extensions build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies for the bridge
RUN pip3 install --no-cache-dir paho-mqtt python-dotenv

# Copy workspace and build the packages (ros_mqtt_bridge, mock_gps, mock_system)
WORKDIR /root/ws
COPY . /root/ws

# Source ROS and build selected packages
RUN . /opt/ros/humble/setup.sh && \
    colcon build --packages-select ros_mqtt_bridge mock_gps mock_system

# Entry: start a shell with the workspace sourced for interactive use
ENTRYPOINT ["/bin/bash","-lc","source /root/ws/install/setup.bash && bash"]
