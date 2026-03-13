from setuptools import setup, find_packages

package_name = 'mock_gps'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='User',
    author_email='user@example.com',
    maintainer='User',
    maintainer_email='user@example.com',
    description='Mock GPS ROS 2 node that publishes location and heading',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'mock_gps = mock_gps.node:main',
        ],
    },
)
