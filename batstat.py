#!/usr/bin/python
import pystray
import time
import psutil

icon = pystray.Icon('batstat')

from PIL import Image, ImageDraw, ImageFont

def create_image(battery_status, power_plugged):
    # Generate an image and draw a pattern
    width = 48
    height = 48
    black = (0, 0, 0)
    orange = (201, 121, 0)
    green = (0, 181, 0)
    red = (201, 0, 0)
    image = Image.new('RGB', (width, height), black)

    if power_plugged:
        bgcolor = green
    elif  battery_status < 20:
        bgcolor = red
    else:
        bgcolor = orange

    bar_height = int(48 - (float(battery_status) / 100)*48)

    dc = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 30)
    dc.rectangle([(0, bar_height), (48, 48)], bgcolor) #str(battery_status) ,(255, 255, 255),font=font)
    dc.text((1, 1), str(battery_status), (255, 255, 255), font=font)

    return image

def setup(icon):
    icon.visible = True
    status = psutil.sensors_battery()
    btstatus = status[0]
    power_plugged = status[2]
    while True:
        if btstatus != status[0] or power_plugged != status[2]:
            btstatus = status[0]
            power_plugged = status[2]
            icon.icon = create_image(int(float(btstatus)), power_plugged)
        time.sleep(5)
        status = psutil.sensors_battery()

status = psutil.sensors_battery()
btstatus = status[0]
power_plugged = status[2]
icon.icon = create_image(int(float(btstatus)), power_plugged)

icon.run(setup)
