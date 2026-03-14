from setuptools import setup, find_packages
from ament_package.templates import get_environment_hook_template_path

package_name = 'mock_gps'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Hvis du har launch-filer, legg dem til slik:
        # ('share/' + package_name + '/launch', ['launch/bridge.launch.py']),
    ],
    install_requires=['setuptools', 'paho-mqtt', 'python-dotenv'],
    zip_safe=True,
    author='User',
    author_email='user@example.com',
    maintainer='User',
    maintainer_email='user@example.com',
    description='Mock GPS ROS 2 node that publishes location and heading',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # 'ros_mqtt_bridge' blir navnet du bruker etter `ros2 run ros_mqtt_bridge ros_mqtt_bridge`
            'mock_gps = mock_gps.node:main',
        ],
    },
)