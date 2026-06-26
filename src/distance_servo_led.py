#!/usr/bin/env python3
"""Drive a servo and 3 LEDs from TF-Luna distance readings on the RDK X5.

Sequence (one stage active at a time):
    d >= 0.80 m         -> servo 135 deg, LED3 on
    0.60 <= d < 0.80 m  -> servo  90 deg, LED2 on
    0.30 <= d < 0.60 m  -> servo  45 deg, LED1 on
    d  < 0.30 m / weak  -> servo   0 deg, all LEDs off

Wiring:
    TF-Luna : I2C bus 5 @ 0x10        (see tfluna_i2c.py)
    Servo   : BOARD pin 18 (PWM)      (see servo_sweep.py)
    LED1    : BOARD pin 11 (GPIO17)   anode -> resistor -> pin, cathode -> GND
    LED2    : BOARD pin 13 (GPIO27)
    LED3    : BOARD pin 15 (GPIO22)

Requires: pip3 install smbus2 ; Hobot.GPIO (system package).
"""

import time

import Hobot.GPIO as GPIO
from smbus2 import SMBus

# --- TF-Luna (from tfluna_i2c.py) ---
I2C_BUS = 5
TFLUNA_ADDR = 0x10
MIN_AMP = 100         # readings below this signal strength are unreliable

# --- Servo (from servo_sweep.py) ---
SERVO_PIN = 18        # BOARD pin 18 -> pwm1 (34150000) ch1; enabled by default
PWM_FREQ_HZ = 50
MIN_DUTY = 2.5        # ~0.5ms pulse -> 0 degrees
MAX_DUTY = 12.5       # ~2.5ms pulse -> 180 degrees

# --- LEDs (BOARD pins) ---
LED_PINS = [11, 13, 15]   # LED1, LED2, LED3

# --- Stage table: (distance threshold in m, servo angle, LED index or None) ---
# Checked from the top down; first match wins.
STAGES = [
    (1.5, 135, 2),   # LED3
    (1.0,  90, 1),   # LED2
    (0.50,  45, 0),   # LED1
]
IDLE_ANGLE = 0


def read_tfluna(bus, addr=TFLUNA_ADDR):
    """Return (distance_m, amplitude, temperature_c)."""
    data = bus.read_i2c_block_data(addr, 0x00, 6)
    dist_cm = data[0] | (data[1] << 8)
    amp     = data[2] | (data[3] << 8)
    temp_c  = (data[4] | (data[5] << 8)) / 100.0
    return dist_cm / 100.0, amp, temp_c


def angle_to_duty(angle: float) -> float:
    angle = max(0.0, min(180.0, angle))
    return MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)


def stage_for(distance_m):
    """Return (servo_angle, active_led_index_or_None) for a distance."""
    for threshold, angle, led_idx in STAGES:
        if distance_m >= threshold:
            return angle, led_idx
    return IDLE_ANGLE, None


def set_leds(active_idx):
    """Light only the LED at active_idx (None = all off)."""
    for i, pin in enumerate(LED_PINS):
        GPIO.output(pin, GPIO.HIGH if i == active_idx else GPIO.LOW)


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PINS, GPIO.OUT, initial=GPIO.LOW)

    servo = GPIO.PWM(SERVO_PIN, PWM_FREQ_HZ)
    servo.start(angle_to_duty(IDLE_ANGLE))

    # Hobot.GPIO bug: PWM.start() gates the "enable" write on the *previous*
    # duty (still 0 right after __init__), so force it on via sysfs.
    enable_path = GPIO.pin_info[SERVO_PIN].pwm_enable
    with open(enable_path, "w") as f:
        f.write("1")
    time.sleep(0.5)

    current_angle = None
    try:
        with SMBus(I2C_BUS) as bus:
            print("Running distance -> servo + LED sequence. Ctrl-C to stop.")
            while True:
                try:
                    distance_m, amp, _ = read_tfluna(bus)
                except OSError as e:
                    print(f"I2C read failed: {e}")
                    time.sleep(0.5)
                    continue

                if amp < MIN_AMP or distance_m <= 0:
                    angle, led_idx = IDLE_ANGLE, None
                    label = "no reliable reading"
                else:
                    angle, led_idx = stage_for(distance_m)
                    label = f"{distance_m:.2f} m"

                set_leds(led_idx)
                # Only command the servo when the target angle changes, so it
                # isn't jittering on every loop.
                if angle != current_angle:
                    servo.ChangeDutyCycle(angle_to_duty(angle))
                    current_angle = angle

                led_str = "off" if led_idx is None else f"LED{led_idx + 1}"
                print(f"{label:<20s} -> servo {angle:3d} deg, {led_str}")
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        servo.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
