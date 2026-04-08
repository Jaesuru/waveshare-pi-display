#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import time
import logging
import socket  
import subprocess 
import psutil # Re-added for RAM usage
import RPi.GPIO as GPIO  
from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd2in7_V2

logging.basicConfig(level=logging.DEBUG)

# --- GPIO SETUP ---
KEY1_PIN = 5  
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SCREEN_WIDTH = 264
SCREEN_HEIGHT = 176

def get_ram_usage():
    """Returns the RAM usage percentage."""
    try:
        usage = psutil.virtual_memory().percent
        return f"RAM: {usage}%"
    except:
        return "RAM: N/A"

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"IP: {ip}"
    except: return "IP: 127.0.0.1"

def get_face_image(root):
    faces = ["face1.bmp", "face2.bmp", "face3.bmp", "face4.bmp", "face5.bmp", "face6.bmp", "face7.bmp", "face8.bmp", "face9.bmp", "face10.bmp"]
    index = int(time.time() / 60) % len(faces)
    img_path = os.path.join(root, "images", faces[index])
    try:
        img = Image.open(img_path).convert('L')
        img = img.point(lambda x: 0 if x < 100 else 255, '1')
    except: img = Image.new('1', (90, 80), 255)
    return img.resize((90, 80))

def get_quote():
    quotes = ["BETTER DAYS TO COME.", "YOU'RE BETTER THAN YESTERDAY.", "MAKE SURE TO STAY HYDRATED!", "COMPARISON IS THE THIEF OF JOY.", "I BELIEVE IN YOU.", "DON'T FORGET TO LOVE YOURSELF.", "EVERYDAY IS A GOOD DAY.", "DON'T FORGET TO TAKE A BREAK.", "SUPER DUPER POOPER", "PIBBLE TIME!!!", "JASON WUZ HERE", "LOCK IN, TWIN!!!", "NO PAIN, NO GAIN.", "FALL A FEW TIMES, STAND UP A LITTLE MORE.", "YOU MISS 100% OF THE SHOTS YOU DON'T TAKE.", "YOU'RE NOT ALONE IN THIS.", "YOU'LL DO JUST FINE, I BELIEVE IT."]
    return quotes[int(time.time() / 3600) % len(quotes)]

def main():
    try:
        time.sleep(5)
        logging.info("Initializing Display...")
        epd = epd2in7_V2.EPD()
        epd.init()
        epd.Clear()

        root = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(root, 'fonts', 'pixel.ttf')

        if not os.path.exists(font_path):
            font_sm = font_md = ImageFont.load_default()
        else:
            font_sm = ImageFont.truetype(font_path, 9)
            font_md = ImageFont.truetype(font_path, 11)

        while True:
            # --- CHECK FOR SHUTDOWN BUTTON ---
            if GPIO.input(KEY1_PIN) == GPIO.LOW:
                logging.info("SHUTDOWN TRIGGERED VIA KEY1")
                image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                draw = ImageDraw.Draw(image)
                draw.text((70, 80), "SHUTTING DOWN...", font=font_md, fill=255)
                epd.display(epd.getbuffer(image))
                
                time.sleep(2)
                epd.Clear()
                epd.sleep()
                os.system("sudo shutdown -h now")
                sys.exit()

            image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 0)
            draw = ImageDraw.Draw(image)

            # --- BORDERS ---
            border_str = "+" + "-" * 25 + "+"
            draw.text((10, 2), border_str, font=font_sm, fill=255)
            draw.text((10, SCREEN_HEIGHT - 20), border_str, font=font_sm, fill=255)

            # --- TOP LEFT (DATE/TIME) ---
            draw.text((15, 18), time.strftime("%a %b %d %Y").upper(), font=font_sm, fill=255)
            draw.text((15, 32), time.strftime("%I:%M %p"), font=font_sm, fill=255)

            # --- TOP RIGHT (RAM + IP) ---
            ram_txt = get_ram_usage()
            ip_txt = get_ip_address()
            start_x_right = 145 # Shifted slightly for a cleaner look
            
            # Draw RAM on top line, IP on bottom line
            draw.text((start_x_right, 18), ram_txt, font=font_sm, fill=255)
            draw.text((start_x_right, 30), ip_txt, font=font_sm, fill=255)

            # --- MIDDLE (FACE) ---
            face_img = get_face_image(root)
            image.paste(face_img, ((SCREEN_WIDTH // 2) - 45, (SCREEN_HEIGHT // 2) - 35))

            # --- BOTTOM (QUOTE) ---
            quote = get_quote()
            cursor = "|" if int(time.time()) % 2 == 0 else " "
            draw.text((15, SCREEN_HEIGHT - 35), f"> {quote} {cursor}", font=font_sm, fill=255)

            logging.info("Updating display...")
            epd.display(epd.getbuffer(image))
            
            for _ in range(60):
                if GPIO.input(KEY1_PIN) == GPIO.LOW:
                    break 
                time.sleep(1)

    except KeyboardInterrupt:
        epd.init()
        epd.Clear()
        epd.sleep()
        GPIO.cleanup()
        sys.exit()

if __name__ == "__main__":
    main()
