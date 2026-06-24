#!/usr/bin/env python3
"""Sweep a standard hobby servo back and forth between 0 and 180 degrees
on the RDK X5's hardware PWM header pin using Hobot.GPIO.
"""

import argparse
import time

import Hobot.GPIO as GPIO

SERVO_PIN = 18  # BOARD pin 18 -> pwm1 (34150000) ch1; enabled by default on the X5 image
PWM_FREQ_HZ = 50  # standard servo control frequency

MIN_DUTY = 2.5   # ~0.5ms pulse -> 0 degrees
MAX_DUTY = 12.5  # ~2.5ms pulse -> 180 degrees


def angle_to_duty(angle: float) -> float:
    angle = max(0.0, min(180.0, angle))
    return MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep a servo 0-180-0 on RDK X5")
    parser.add_argument("--pin", type=int, default=SERVO_PIN, help="BOARD pin number")
    parser.add_argument("--cycles", type=int, default=10, help="number of back-and-forth sweeps")
    parser.add_argument("--step-delay", type=float, default=0.02, help="seconds between each 1-degree step")
    args = parser.parse_args()

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    servo = GPIO.PWM(args.pin, PWM_FREQ_HZ)
    servo.start(angle_to_duty(0))

    # Hobot.GPIO bug: PWM.start() gates the sysfs "enable" write on the
    # *previous* duty cycle (still 0 right after __init__), so the channel
    # never actually turns on. Force it directly via sysfs as a workaround.
    enable_path = GPIO.pin_info[args.pin].pwm_enable
    with open(enable_path, "w") as f:
        f.write("1")

    time.sleep(0.5)

    try:
        for cycle in range(args.cycles):
            print(f"cycle {cycle + 1}/{args.cycles}: 0 -> 180")
            for angle in range(0, 181, 1):
                servo.ChangeDutyCycle(angle_to_duty(angle))
                time.sleep(args.step_delay)

            print(f"cycle {cycle + 1}/{args.cycles}: 180 -> 0")
            for angle in range(180, -1, -1):
                servo.ChangeDutyCycle(angle_to_duty(angle))
                time.sleep(args.step_delay)
    except KeyboardInterrupt:
        pass
    finally:
        servo.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
