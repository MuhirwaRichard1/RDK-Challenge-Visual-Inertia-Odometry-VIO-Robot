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

![Flash progress and log](screenshots/01-flash-progress.png)

> Note: the log line reads `Verify: 跳过校验` ("verification skipped"), so the checksum/verify pass itself was bypassed by the tool rather than confirmed — worth knowing if a reviewer asks specifically about verified writes.

The flasher then reported the flash as finished:

![Flashing complete](screenshots/02-flash-complete.png)

**Boot evidence:** Remote Desktop session into the board shows it booted past flashing into a working desktop environment (D-Robotics splash/desktop, application launcher visible), confirming a successful boot:

![Board booted to desktop](screenshots/05-desktop-boot.png)

---

## 2. Network connectivity ⚠️ Partial evidence

The board is reachable on the LAN — RDK Studio's Workspace view shows a live "Connected" session over SSH at `192.168.128.10` with live MEM/TEMP/CPU/BPU/DISK telemetry, which requires the board to have a working IP and be reachable from the PC:

![Workspace connected with live metrics](screenshots/03-workspace-connected.png)

**Gap:** none of the current screenshots show an explicit outbound check from *inside* the board (e.g. `ping 8.8.8.8` or `curl -I https://example.com`) proving internet + DNS resolution, which is what the challenge's standard of completion asks for. Recommend grabbing one more terminal screenshot running something like:

```bash
ping -c 4 8.8.8.8
curl -I https://www.google.com
```

---

## 3. SSH login ✅ Mostly complete

Opened an interactive SSH shell from the PC to the board via RDK Studio's Terminal panel. Welcome banner confirms `Ubuntu 22.04.5 LTS (GNU/Linux 6.1.83 aarch64)`, and a command (`ls`) was run successfully at the `root@ubuntu:~#` prompt:

![SSH terminal session](screenshots/04-ssh-terminal.png)

**Gap:** the challenge calls out `uname -a` and `htop` specifically as example commands. The screenshot only shows `ls`. Worth re-running and capturing `uname -a` (and optionally `htop`) for a screenshot that matches the wording exactly.

---

## 4. Community connection ❌ Not yet provided

No evidence of joining the official RDK Discord (or announced channel) or completing the Stage 1 check-in template is included yet.

**Action needed:** join the channel, post the self-introduction / check-in, and add the permalink here:

```
Check-in permalink: <paste link here>
```

---

## Summary

| # | Task | Status | Evidence |
|---|------|--------|----------|
| 1 | System image flash | ✅ Complete | `01-flash-progress.png`, `02-flash-complete.png`, `05-desktop-boot.png` |
| 2 | Network connectivity | ⚠️ LAN reachability shown; public internet ping/curl not yet captured | `03-workspace-connected.png` |
| 3 | SSH login | ✅ Shell access shown; exact example commands (`uname -a`, `htop`) not yet captured | `04-ssh-terminal.png` |
| 4 | Community connection | ❌ Missing | — |

