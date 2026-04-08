# 📺 Waveshare 2.7" e-Paper (Raspberry Pi Zero WH)

A minimal Python setup to transform your Raspberry Pi Zero WH into a terminal-style status display using the Waveshare 2.7" e-Paper (V2).

---

## Requirements
* **Hardware:** Raspberry Pi Zero WH
* **Display:** [Waveshare 2.7" e-Paper (V2)](https://www.waveshare.com/2.7inch-e-paper-hat.htm)
* **Storage:** MicroSD card (8GB+)
* **OS:** Raspberry Pi OS (Lite recommended)

---

## Directory Structure
Ensure your project folder is organized like this for the script to find your assets:
```text
terminal_display/
├── main.py
├── fonts/
│   └── pixel.ttf
└── images/
    ├── face1.bmp
    └── face2.bmp

## Setup
1. Flash OS & Connect
Flash your SD card using Raspberry Pi Imager. Configure SSH and Wi-Fi in the advanced settings.

Bash
ssh pi@raspberrypi.local
