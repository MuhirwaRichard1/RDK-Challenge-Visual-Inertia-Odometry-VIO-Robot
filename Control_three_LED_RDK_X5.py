#!/usr/bin/env python3
import Hobot.GPIO as GPIO
import time

LED_PINS = [11, 13, 15]

GPIO.setmode(GPIO.BOARD)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)

try:
    print("Testing LEDs one by one ...")
    for i, pin in enumerate(LED_PINS, 1):
        print(f"  LED {i} ON (Pin {pin})")
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.8)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.3)

    print("All LEDs blinking together ...")
    for _ in range(5):
        for pin in LED_PINS:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        for pin in LED_PINS:
            GPIO.output(pin, GPIO.LOW)
        time.sleep(0.3)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print("Done.")
