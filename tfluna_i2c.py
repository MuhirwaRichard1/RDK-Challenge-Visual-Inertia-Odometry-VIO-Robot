#!/usr/bin/env python3
"""
Read distance (in meters) from a Benewake TF-Luna in I2C mode on the RDK X5.

Wiring (TF-Luna 6-pin -> RDK X5 40-pin header):
    Pin 1 VCC     -> 5V   (header pin 2 or 4)
    Pin 2 SDA     -> SDA  (header pin 3)
    Pin 3 SCL     -> SCL  (header pin 5)
    Pin 4 GND     -> GND  (header pin 6)
    Pin 5 config  -> GND  (ties low to select I2C mode)
    Pin 6         -> not connected

Requires: pip3 install smbus2   (and: sudo apt install -y i2c-tools)
Confirm the bus first with:  sudo i2cdetect -y -r 0   (look for 0x10)
"""

import time
from smbus2 import SMBus

I2C_BUS = 5           # 40-pin header pins 3/5 = SoC I2C5 -> /dev/i2c-5 (enable via srpi-config) for rdk x5
TFLUNA_ADDR = 0x10    # TF-Luna default I2C address
MIN_AMP = 100         # readings below this signal strength are unreliable


def read_tfluna(bus, addr=TFLUNA_ADDR):
    """Return (distance_m, amplitude, temperature_c)."""
    # 6 bytes from reg 0x00: DIST_L, DIST_H, AMP_L, AMP_H, TEMP_L, TEMP_H
    data = bus.read_i2c_block_data(addr, 0x00, 6)

    dist_cm = data[0] | (data[1] << 8)              # distance in centimeters
    amp     = data[2] | (data[3] << 8)              # signal strength
    temp_c  = (data[4] | (data[5] << 8)) / 100.0    # chip temperature, 0.01 C units

    return dist_cm / 100.0, amp, temp_c


def main():
    with SMBus(I2C_BUS) as bus:
        print(f"Reading TF-Luna at 0x{TFLUNA_ADDR:02X} on i2c-{I2C_BUS}. Ctrl-C to stop.")
        while True:
            try:
                distance_m, amp, temp_c = read_tfluna(bus)
            except OSError as e:
                print(f"I2C read failed: {e} (check wiring / bus number)")
                time.sleep(0.5)
                continue

            # Dead zone is < 0.2 m; a weak/zero return means no reliable target.
            if amp < MIN_AMP or distance_m <= 0:
                print("-- no reliable reading (signal weak or out of range)")
            else:
                print(f"Distance: {distance_m:5.2f} m   amp={amp:<6d} temp={temp_c:.1f} C")

            time.sleep(0.1)   # 10 Hz; TF-Luna's default internal rate is 100 Hz


if __name__ == "__main__":
    main()