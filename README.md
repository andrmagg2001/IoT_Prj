# Smart Traffic Light - IoT Project

## Overview
This project implements a **smart traffic light system** using **Raspberry Pi** as the central processing unit and **Arduino** as the actuator for the traffic lights (LEDs).  
The Raspberry Pi runs the traffic optimization algorithm, while the Arduino controls the physical LEDs according to the decisions received.

The system can be extended with a **video module** (via webcam and OpenCV) to estimate real traffic conditions in real time.

---

## Architecture
- **Raspberry Pi**  
  - Runs the traffic simulation and optimization (Markov Decision Process or Reinforcement Learning).  
  - Communicates the optimal action (which light should be green) to the Arduino via serial.  

- **Arduino**  
  - Receives commands from the Raspberry Pi (`G1`, `G2`).  
  - Controls the physical LEDs (traffic lights).  

- **Optional Video Module**  
  - Raspberry Pi + camera + OpenCV to detect and count cars.  
  - Real traffic counts can replace or integrate with the simulation.  

---

## Traffic Model
- Two roads: **r1** and **r2**, each ending with a traffic light.  
- At each time step:
  - Cars can **arrive randomly** (up to 5 for r1, up to 3 for r2).  
  - A limited number of cars can **leave the road** when the light is green (max 3 for r1, max 2 for r2).  
- Each state is defined as:  
    s = (n1,n2,TL1,TL2,N)

    where:
    - `n1`: cars on road r1 (max 40)  
    - `n2`: cars on road r2 (max 25)  
    - `TL1`, `TL2`: traffic lights (green/red)  
    - `N`: total traffic (n1 + n2)

- **Reward function**:  
- `+1` if traffic is low (N < 15)  
- `0` if traffic is medium (15 ≤ N < 30)  
- `-1` if traffic is high (N ≥ 30)

---

## Features
- Simulation of traffic congestion using a **Markov Decision Process**.  
- Implementation of an **optimization algorithm** (Value Iteration, Q-learning, or similar).  
- Real-time control of **physical LEDs** via Arduino.  
- Data logging and visualization (reward trend, traffic states).  
- Optional integration with **computer vision** to detect real cars.  

---

## Requirements
- **Hardware**:
- Raspberry Pi (any model with Python support)
- Arduino (Uno or similar)
- LEDs (Red, Green, Yellow optional) + resistors
- USB cable for Pi ↔ Arduino connection
- Webcam (optional)

- **Software**:
- Python 3 (`numpy`, `matplotlib`, `pyserial`, `opencv-python` for video module)
- Arduino IDE

---

## How It Works
1. **Simulation**: Raspberry simulates or captures the number of cars on each road.  
2. **Optimization**: The algorithm decides which traffic light should be green.  
3. **Communication**: Raspberry sends the decision (`G1` or `G2`) to the Arduino.  
4. **Execution**: Arduino turns on the corresponding LED.  
5. **(Optional)**: Real cars are counted using OpenCV instead of simulation.  

---

## Demo
- Raspberry Pi running the optimization algorithm.  
- Arduino traffic lights switching automatically to reduce congestion.  
- Graphs showing traffic levels and rewards over time.  

---

## Future Improvements
- Extend the model to **multiple intersections**.  
- Use **deep reinforcement learning** for more complex policies.  
- Deploy a **dashboard** for live monitoring.  

---

## Author
Andrea Maggiore – IoT student project (Sapienza University of Rome).
