### Challenge 2 — Sensor Explorer

Demonstrate hands-on I/O by **successfully driving or reading** at least **one** of the following categories on RDK X5 (hardware or officially supported accessory as applicable):

- Camera  
- IMU  
- GPIO  
- Microphone  
- Motor (driver + motor or actuator kit)

**Standard of completion:**  
- A **short log or photo** showing the sensor/actuator responding (e.g. camera preview window, IMU stream values, GPIO toggling LED, mic level meter, motor spin).  
- Brief note in your repo **which interface** you used (e.g. MIPI, I2C, sysfs, ROS 2 node name).

---
40-PIN HEADER (RDK X5)
┌─────────────────────┐
│  1  🟡 3.3V  │  2  🟡 5V     │
│  3  🟡 SDA   │  4  🟡 5V     │  ← TF-Luna: VCC→Pin1 or Pin2
│  5  🟡 SCL   │  6  ⚫ GND    │            SDA→Pin3, SCL→Pin5, GND→Pin6
│  7          │  8          │
│  9  ⚫ GND   │ 10          │
│ 11  🔵 LED1  │ 12          │  ← LED1 anode→Pin11 (via 330Ω)
│ 13  🔵 LED2  │ 14  ⚫ GND   │  ← LED2 anode→Pin13 (via 330Ω)
│ 15  🔵 LED3  │ 16          │  ← LED3 anode→Pin15 (via 330Ω)
│ ...          │ ...         │
│ 32  🔴 Servo │ 33          │  ← Servo signal→Pin32
│ 34  ⚫ GND   │ ...         │  ← Servo GND→Pin34 (common ground)
└─────────────────────┘

```
cd /userdata/rdkstudio/projects/studio-default-project
```
