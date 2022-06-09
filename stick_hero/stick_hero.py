from ppadb.client import Client
from PIL import Image
import sys
import numpy
import time

# to print without truncating
numpy.set_printoptions(threshold=sys.maxsize)

# connecting and selecting a device
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()
if len(devices) == 0:
    print("no device attached")
    quit()
device = devices[0]

while True:

    # screeshot storage and to numpy array
    image = device.screencap()
    with open("screen.png", "wb") as f:
        f.write(image)
    image = Image.open("screen.png")
    image = numpy.array(image, dtype=numpy.uint8)

    # list of list of each pixel rgb in row 1725
    pixels = [list(i[:3]) for i in image[1925]]

    # to store black->color and black->color
    transitions = []

    ignore_first_colors = True
    black = True
    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        if ignore_first_colors and (r + g + b) != 0:
            continue
        ignore_first_colors = False

        if black and (r + g + b) != 0:
            black = not black
            transitions.append(i)
            continue
        if not black and (r + g + b) == 0:
            black = not black
            transitions.append(i)
            continue

    if len(transitions) == 0:
        transitions.append(1080)

    start, target1, target2 = transitions
    distance = (target1 + target2) / 2 - start
    distance = distance * 0.98

    device.shell(f"input touchscreen swipe 500 500 500 500 {int(distance)}")
    time.sleep(3)
