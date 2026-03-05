# CME Research Robot Descriptions

This package contains URDF/Xacro descriptions for various robots developed by CME Robotics. It provides 3D models, physical properties, and controller configurations for simulation and visualization in ROS environments.


# ROS Distro Support #


|         |                                           melodic                                            |      noetic      |                  rolling                  |
|:-------:|:--------------------------------------------------------------------------------------------:|:----------------:|:-----------------------------------------:|
| Branch  | [`melodic_dev`](https://bitbucket.org/cme-robotics/cmeresearch_description/src/melodic_dev/) |                  |   [`rolling_dev`] |
| Status  |                                          supported                                           |  not supported   |  supported |
| Version |                                       no yet released                                        | not yet released |    not yet released |




## Robot Models

The package includes the following robot models:

- **CMEXA**: A small mecanum drive robot (0.2m x 0.13m x 0.15m) capable of holonomic motion.
- **CMEXAIII**: An updated version of the CMEXA robot with similar mecanum drive capabilities.
- **ASH**: A four-wheeled robot with a laser sensor.
- **UnicoMini**: A compact mobile robot platform.

Each robot model includes:
- URDF/Xacro description files
- STL mesh files for visualization and collision detection
- Physical properties (dimensions, mass, inertia)
- Gazebo simulation configurations

## Installation

### Prerequisites

- ROS1 (melodiv) or ROS2 (rolling)
- xacro package
- robot_state_publisher package

### Building from Source

1. Clone this repository into your ROS workspace:
   ```bash
   cd ~/ros2_ws/src
   git clone https://github.com/cmerobotics/cmeresearch_description.git
   ```

2. Build the package:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select cmeresearch_description
   ```

3. Source the workspace:
   ```bash
   source ~/ros2_ws/install/setup.bash
   ```

### Docker

The package includes Docker configurations for both amd64 and arm64v8 architectures:

- For amd64:
  ```bash
  cd docker/amd64
  ./build.sh
  ./run.sh
  ```

- For arm64v8:
  ```bash
  cd docker/arm64v8
  ./build.sh
  ./run.sh
  ```

## Usage

### Visualizing Robot Models

To visualize a robot model in RViz:

#### ROS1
```bash
roslaunch cmeresearch_description description.launch robot:=cmexa
```

#### ROS2
```bash
ros2 launch cmeresearch_description cmexaiii_mecanum.launch.py gui:=true
```

### Simulation

The package includes Gazebo configurations for simulating the robots. Controllers are provided for the mecanum drive robots, allowing them to be controlled via the `/cmd_vel` topic.

## License

This package is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions to improve the robot descriptions or fix issues are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact

For more information, please contact:
- Email: info@cme-robotics.com
- Website: https://cme-robotics.com

Last updated: August 2, 2025