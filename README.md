# PID-Controlled Submarine Simulation

A realistic submarine depth control simulation using PID (Proportional-Integral-Derivative) controller implemented with Pygame. The simulation demonstrates the principles of buoyancy, depth control, and PID control systems.

## Features

- Real-time submarine depth control simulation
- PID controller with adjustable parameters
- Physics-based movement system including:
  - Buoyancy forces
  - Gravity effects
  - Water drag
  - Air level management
- Interactive controls for depth adjustment
- Real-time visualization of:
  - Current depth
  - Target depth
  - Air level percentage
  - PID parameters

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python 3.x installed on your system
2. Install Pygame using pip:
```bash
pip install pygame
```
3. Clone or download this repository
4. Optionally, place a custom submarine image named 'submarine.png' in the project directory

## Controls

- **Up Arrow**: Decrease target depth (move submarine up)
- **Down Arrow**: Increase target depth (move submarine down)
- **R Key**: Reset simulation
- **Mouse**: Click on PID parameters (KP, KI, KD) to modify their values
- **Enter**: Confirm PID parameter changes
- **Backspace**: Delete input when modifying PID parameters

## Physical Model

The simulation implements a realistic physical model including:

- Buoyancy force proportional to submarine's air level
- Gravity effects
- Water drag (quadratic with velocity)
- Air level management system

### Air Control System

The submarine uses an automatic air control system that:
- Decreases air level when diving deeper
- Increases air level when surfacing
- Maintains optimal air level for neutral buoyancy at target depth
- Uses PID control for precise depth maintenance

## PID Controller

The simulation uses a PID controller to maintain the submarine's depth by managing air levels. Default PID parameters are:

- KP (Proportional Gain): 0.5
- KI (Integral Gain): 0.003
- KD (Derivative Gain): 0.8

These parameters can be adjusted in real-time to observe different control behaviors:
- Higher KP: More aggressive response to depth errors
- Higher KI: Better steady-state error elimination
- Higher KD: Better damping of oscillations

## Display Information

The simulation displays real-time information including:
- Current air level in the submarine (%)
- Target depth (meters)
- Current depth (meters)
- PID parameters with adjustable values

## Customization

You can customize various aspects of the simulation by modifying the constants in the code:

- Screen dimensions (SCREEN_WIDTH, SCREEN_HEIGHT)
- Physical parameters (BUOYANCY_FACTOR, GRAVITY, DRAG)
- PID parameters (KP, KI, KD)
- Air change rate (AIR_CHANGE_RATE)

## Troubleshooting

1. If the submarine movement seems too sensitive:
   - Decrease the PID parameters
   - Adjust the BUOYANCY_FACTOR or DRAG values

2. If the submarine oscillates too much:
   - Increase the KD parameter
   - Decrease the KP parameter
   - Adjust the AIR_CHANGE_RATE

3. If the submarine responds too slowly:
   - Increase the KP parameter
   - Decrease the DRAG value
   - Increase the AIR_CHANGE_RATE

## License

This project is released under the MIT License. Feel free to use, modify, and distribute it as you see fit.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## Acknowledgments

This simulation was created as an educational tool to demonstrate:
- PID control systems
- Buoyancy physics
- Real-time control systems
- Python game development with Pygame
