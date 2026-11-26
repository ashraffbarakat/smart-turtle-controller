# Smart Turtle Controller

A modular ROS 2-based robotics project that demonstrates structured robot control and inter-package communication using Turtlesim.

The system allows users to control a simulated turtle and draw different geometric shapes, including circles, squares, and spirals, through configurable commands and an interactive graphical interface.

Built with **ROS 2 Jazzy**, **Python**, and **Tkinter**, the project demonstrates essential ROS 2 concepts through a practical multi-package architecture.

### Key Features

- Custom ROS 2 message interfaces.
- Shape-based motion control (Circle, Square, Spiral).
- Configurable linear and angular velocities.
- Periodic command publishing.
- Automated simulation reset.
- Interactive Tkinter GUI.
- YAML-based configuration.
- Unified system startup using ROS 2 Launch.
- ROS 2 communication monitoring using RQT.

### Technology Stack

- ROS 2 Jazzy
- Ubuntu 24.04 LTS
- Python
- Tkinter
- Turtlesim
- Colcon
- YAML
- RQT

### Project Architecture

The system consists of three ROS 2 packages:

1. `smart_turtle_interface` – Defines custom communication messages.
2. `smart_turtle_py` – Implements the control logic and GUI nodes.
3. `smart_turtle_bringup` – Manages configuration and system launch.

### License

This project is licensed under the MIT License.
