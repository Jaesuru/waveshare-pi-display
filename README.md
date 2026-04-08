# Waveshare 2.7" e-Paper (Raspberry Pi Zero WH)

A minimal Python setup to turn your Raspberry Pi Zero WH into a terminal-style status display using the Waveshare 2.7" e-Paper (V2).

## Step 1: Flash Raspberry Pi OS

Use Raspberry Pi Imager on another computer and select Raspberry Pi OS Lite (32-bit), then flash it to your SD card. Before ejecting the card, make sure SSH is enabled and configure Wi-Fi using the network configuration settings (either through the imager’s advanced options or by editing the network-config file).

## Step 2: Connect via SSH

Find your Raspberry Pi’s IP address using a method like `arp -a`, then connect from your computer’s terminal using either `ssh pi@<IP_ADDRESS>` or `ssh pi@raspberrypi.local`.

## Step 3: Enable SPI

Once connected over SSH, run `sudo raspi-config`, navigate to Interface Options, then SPI, and enable it. After enabling SPI, reboot the device using `sudo reboot`.

## Step 4: Install Dependencies

Update and upgrade your system packages, then install the required Python dependencies. Run `sudo apt update && sudo apt upgrade -y`, followed by `sudo apt install python3-pip python3-pil python3-numpy -y`, and then install psutil using `pip3 install psutil`.

## Step 5: Install Waveshare Drivers

Clone the Waveshare e-Paper repository using `git clone https://github.com/waveshare/e-Paper.git`, then navigate into the Python driver directory with `cd e-Paper/RaspberryPi_JetsonNano/python` and install it using `sudo python3 setup.py install`.

## Step 6: Set Up Project Directory

Navigate to your home directory, create a new project folder, and open your main script file by running `cd ~`, `mkdir terminal_display`, `cd terminal_display`, and `nano main.py`. Paste your display code into this file and save it.

## Step 7: Test the Display

To confirm the display is working correctly, navigate to the examples directory using `cd ~/e-Paper/RaspberryPi_JetsonNano/python/examples` and run the test script with `python3 epd_2in7_V2_test.py`.

## Step 8: Run Your Script

Once the display test is successful, go back to your project directory using `cd ~/terminal_display` and run your script with `python3 main.py`.

## Step 9: Optional - Run on Boot

To automatically run your script at startup, open the crontab editor using `crontab -e` and add the line `@reboot python3 /home/pi/terminal_display/main.py &` to the file.

## Step 10: Notes

You can use any hardware setup or enclosure you prefer depending on your project goals. This setup is intended as a simple and customizable terminal-style display project built for flexibility and experimentation. \n

honoroable mentionz: chatgpt \n

also keep in mind that the pi is set to power on as soon its connected to power. make sure to properly shut it down to prevent sd corruption by pressing on key1 button on the left (hold it for 3 seconds) \n

the network information can again, be configured through the sd card plugged into your computer, and editing the network-config file. All you have to do is add your SSID (network name) and password in a json-like format - if you dont know how to do it, just chatgpt it lol. If that doesn't all work, you'll need an hdmi to mini hdmi cable to link it up to a monitor and use a usb b keyboard... which requires an adapter. ok point besides that, its complicated and its better to just ssh into it.
