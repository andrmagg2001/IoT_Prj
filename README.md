# IoT project - smart traffic light 🚦

Modern intersections still rely on **fixed-time traffic lights**, which ignore real, fluctuating demand. This project delivers a **smart, vision-driven traffic light** where a **Raspberry Pi** acts as the **central analysis server**, estimates vehicle queues with computer vision, and dynamically allocates green time to the busier approach—improving **flow, fairness, and safety** without expensive roadside sensors.

### Approach
- **Perception:** The Raspberry Pi runs a lightweight **YOLOv8** model to detect and count vehicles from cameras (or test images), smoothing counts over a short window to remove jitter.
- **Policy:** An adaptive controller enforces **minimum/maximum green** and **safety transitions** (yellow → all-red), and switches early only when the opposite queue clearly dominates.
- **Actuation:** Commands are sent over **TCP** to an edge controller (Arduino/ESP32) that drives the physical LEDs.

### Architecture at a Glance
- **Raspberry Pi (central brain):** vision inference, queue smoothing, phase logic, TCP client.  
- **Arduino/ESP32 (edge controller):** Wi-Fi AP + **TCP server on port 8080**, line-based protocol with **ACK** replies, safe transitions, deterministic pin control.



## Arduino Part
[Code of Arduino Part](Arduino/Setup_Arduino/Setup_Arduino.ino)


## Raspberry Part

[Code and Server Architecture Overview](Raspberry/central_brain.ipynb)