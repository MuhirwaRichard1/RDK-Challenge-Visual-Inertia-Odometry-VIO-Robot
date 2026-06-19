# Challenge 1 — Board Bring-Up ("Wake the board")

**Device:** RDK X5 / X5 Module
**Tool used:** RDK Studio v1.2.3
**OS image:** RDKOS 3.5.0 Desktop (Ubuntu 22.04.5 LTS, kernel 6.1.83 aarch64)
**Board IP:** 192.168.128.10 (connection profile "RDK X5 (闪连)")

---

## 1. System image flash ✅ Complete

Flashed using RDK Studio's **Flasher** tool:

- Device: `RDK X5 / X5 Module`
- Image: `RDKOS 3.5.0 Desktop`
- Steps Download → Decompress → Write → Verify all reported **Done**, write reached 9912.0 MB / 9912.0 MB (100%).

![Flash progress and log](Screenshot/01-flash-progress.png)

> Note: the log line reads `Verify: 跳过校验` ("verification skipped"), so the checksum/verify pass itself was bypassed by the tool rather than confirmed — worth knowing if a reviewer asks specifically about verified writes.

The flasher then reported the flash as finished:

![Flashing complete](Screenshot/02-flash-complete.png)

**Boot evidence:** Remote Desktop session into the board shows it booted past flashing into a working desktop environment (D-Robotics splash/desktop, application launcher visible), confirming a successful boot:

![Board booted to desktop](Screenshot/05-desktop-boot.png)


---

## 3. SSH login ✅ Mostly complete

Opened an interactive SSH shell from the PC to the board via RDK Studio's Terminal panel. Welcome banner confirms `Ubuntu 22.04.5 LTS (GNU/Linux 6.1.83 aarch64)`, and a command (`ls`) was run successfully at the `root@ubuntu:~#` prompt:

![SSH terminal session](Screenshot/04-ssh-terminal.png)

**Gap:** the challenge calls out `uname -a` and `htop` specifically as example commands. The screenshot only shows `ls`. Worth re-running and capturing `uname -a` (and optionally `htop`) for a screenshot that matches the wording exactly.

---

## Summary

| # | Task | Status | Evidence |
|---|------|--------|----------|
| 1 | System image flash | ✅ Complete | `01-flash-progress.png`, `02-flash-complete.png`, `05-desktop-boot.png` |
| 2 | SSH login | ✅ Shell access shown; exact example commands (`uname -a`, `htop`) not yet captured | `04-ssh-terminal.png` |

