# RDK X5 Peripherals — Distance-Driven Servo + LEDs

This project reads distance from a **Benewake TF-Luna** (I2C mode) and uses it to
drive a **hobby servo** and **three LEDs** through staged thresholds.

Main script: [`distance_servo_led.py`](distance_servo_led.py)
Helper test scripts: [`tfluna_i2c.py`](tfluna_i2c.py) (sensor only),
[`servo_sweep.py`](servo_sweep.py) (servo only).

---

## What it does

The loop reads the TF-Luna ~10 times a second and picks one stage based on the
measured distance. Exactly one stage is active at a time (the servo can only hold
one angle), so only that stage's LED is lit:

| Distance (m)        | Servo angle | LED on        |
|---------------------|-------------|---------------|
| `d >= 1.5`          | 135°        | LED3 (pin 15) |
| `1.0 <= d < 1.5`    | 90°         | LED2 (pin 13) |
| `0.5 <= d < 1.0`    | 45°         | LED1 (pin 11) |
| `d < 0.5` / no read | 0°          | all off       |

> These thresholds live in the `STAGES` table near the top of
> `distance_servo_led.py` — edit that one place to retune the distances, angles,
> or LED mapping. A reading with signal strength below `MIN_AMP` (100) or
> distance `<= 0` is treated as "no reliable reading" and falls back to idle.

---

## Hardware wiring (40-pin header, BOARD numbering)

| Peripheral | Signal        | Header pin | Notes                                   |
|------------|---------------|-----------|------------------------------------------|
| TF-Luna    | VCC           | 2 or 4    | 5V                                       |
| TF-Luna    | SDA           | 3         | I2C5_SDA                                 |
| TF-Luna    | SCL           | 5         | I2C5_SCL                                 |
| TF-Luna    | GND           | 6         |                                          |
| TF-Luna    | config (pin 5)| GND       | tie low to select I2C mode               |
| Servo      | signal        | **18**    | pwm1 (34150000) ch1 — PWM-capable        |
| Servo      | V+            | 2 or 4    | 5V (see power note below)                |
| Servo      | GND           | 6 / 9 …   | must share GND with the board            |
| LED1       | anode         | 11        | GPIO17 → resistor (~330 Ω) → LED → GND   |
| LED2       | anode         | 13        | GPIO27 → resistor → LED → GND            |
| LED3       | anode         | 15        | GPIO22 → resistor → LED → GND            |

**LED orientation:** each GPIO pin → current-limiting resistor (~330 Ω) →
LED anode (long leg); LED cathode (short leg) → GND.

### Wiring diagram

```
        RDK X5 40-pin header (BOARD numbering, pin 1 top-left)
        odd pins = left column, even pins = right column

                          +-----+-----+
                     3V3  |  1  |  2  |  5V  ----+------------> Servo V+
        TF-Luna SDA <---  |  3  |  4  |  5V      +-----------> TF-Luna VCC
        TF-Luna SCL <---  |  5  |  6  |  GND ----+--+--------> TF-Luna GND
                   GPIO7  |  7  |  8  |  TXD     |  +--------> TF-Luna config (tie low)
                     GND  |  9  | 10  |  RXD     |
        LED1 +--[330R]--  | 11  | 12  |  GPIO    +-----------> Servo GND
        LED2 +--[330R]--  | 13  | 14  |  GND
        LED3 +--[330R]--  | 15  | 16  |  GPIO
                     3V3  | 17  | 18  |  <--- Servo signal (PWM)
                SPI_MOSI  | 19  | 20  |  GND
                  ...     | ..  | ..  |  ...
                          +-----+-----+

  LED detail (x3, one per pin 11 / 13 / 15):

      pin --->|---[330R]---+
            (GPIO)         |
                          GND        |>|  = LED, flat/short leg = cathode -> GND

  Servo (3-wire):
      signal (orange/white) ---> pin 18
      V+     (red)          ---> 5V  (pin 2 or 4)
      GND    (brown/black)  ---> GND (pin 6 or 9)   [common ground required]
```

**Servo power:** a small servo can run off the board's 5V for light loads, but
servos draw current spikes that can brown out the board. For anything beyond a
tiny servo, power it from a separate 5V supply and connect that supply's GND to
a board GND pin (common ground is required).

---

## Why servo signal is on pin 18 (not pin 33)

The X5 has four PWM controllers. On the default image, **pwm0/pwm1/pwm2 are
enabled** but **pwm3 (the controller behind header pins 32 and 33) is disabled**,
so pin 33 fails with:

```
FileNotFoundError: .../34170000.pwm/export
```

Pin **18** maps to `pwm1` (`34150000`, channel 1), which is enabled by default —
so it works with no config change and no reboot. Other already-live PWM pins:
29, 31, 37 (and 27, 28).

If you prefer to use pin 33, enable its controller with `sudo srpi-config`
(enable `pwm3`, which disables `i2c1` — harmless here since the TF-Luna is on
i2c5), then reboot. After reboot a new `pwmchip` for `34170000.pwm` appears
under `/sys/class/pwm/`.

---

## One-time setup

1. **Enable I2C5** for the 40-pin header (if not already):

   ```bash
   sudo srpi-config        # Interface/Peripheral config -> enable i2c5
   ```

2. **Install I2C tools and the Python deps:**

   ```bash
   sudo apt install -y i2c-tools
   pip3 install -r requirements.txt
   ```

   `Hobot.GPIO` ships with the RDK X5 system image (no pip install needed), so
   it is not in `requirements.txt`.

3. **Confirm the sensor is on the bus** — look for address `0x10`:

   ```bash
   sudo i2cdetect -y -r 5
   ```

---

## Bench-test each peripheral first

Test the sensor on its own:

```bash
python3 tfluna_i2c.py        # prints distance / amplitude / temperature
```

Test the servo on its own (sweeps 0°→180°→0°):

```bash
python3 servo_sweep.py --cycles 2
```

Both scripts default to the same pins as the combined script, so if they work
individually the combined run will too.

---

## Run the combined sequence

```bash
python3 distance_servo_led.py
```

Sample output:

```
Running distance -> servo + LED sequence. Ctrl-C to stop.
0.42 m               -> servo   0 deg, off
0.73 m               -> servo  45 deg, LED1
1.21 m               -> servo  90 deg, LED2
1.80 m               -> servo 135 deg, LED3
no reliable reading  -> servo   0 deg, off
```

Stop with **Ctrl-C** — the script calls `servo.stop()` and `GPIO.cleanup()` on
exit so the pins are released cleanly.

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `FileNotFoundError: .../34170000.pwm/export` | Servo on pin 33; move signal to pin 18, or enable `pwm3` via `srpi-config`. |
| `I2C read failed` / nothing at `0x10` | Check I2C5 is enabled, wiring on pins 3/5, and the TF-Luna config pin is tied to GND. Re-run `i2cdetect -y -r 5`. |
| `no reliable reading` at close range | TF-Luna's reliable minimum is ~0.2 m; readings below that (or weak `amp`) are rejected. |
| Servo jitters or won't hold | Power the servo from a dedicated 5V supply with a shared ground. |
| LED never lights | Check resistor + LED orientation (anode to GPIO side), and that the pin is in `LED_PINS`. |
| Permission denied on PWM/GPIO sysfs | Run with the user that owns the gpio/pwm udev groups, or use `sudo`. |
```
