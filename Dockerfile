FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

# Minimal build tools, rosdep and colcon
RUN apt-get update && apt-get install -y \
    python3-pip python3-colcon-common-extensions build-essential python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies for the bridge
RUN pip3 install --no-cache-dir paho-mqtt python-dotenv

# Copy workspace and build the packages (ros_mqtt_bridge, mock_gps, mock_system)
WORKDIR /root/ws
COPY . /root/ws

# Initialize rosdep and install OS dependencies for packages (best-effort)
# Allow failures in CI-less environments; errors will be visible during build
RUN rosdep init || true && rosdep update || true && \
    rosdep install -i --from-paths src --rosdistro humble -y || true

# Source ROS and build selected packages
RUN . /opt/ros/humble/setup.sh && \
    colcon build --packages-select ros_mqtt_bridge mock_gps mock_system

# Entry: start a shell with the workspace sourced for interactive use
ENTRYPOINT ["/bin/bash","-lc","source /opt/ros/humble/setup.bash && source /root/ws/install/setup.bash && bash"]
