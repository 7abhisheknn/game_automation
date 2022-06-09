from ppadb.client import Client
from PIL import Image
import sys
import numpy as np
import time
import cv2
from matplotlib import pyplot as plt

# to print without truncating
np.set_printoptions(threshold=sys.maxsize)

# connecting and selecting a device
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()
if len(devices) == 0:
    print("no device attached")
    quit()
device = devices[0]


image = device.screencap()
with open("screen.png", "wb") as f:
    f.write(image)


# Read image.
img = cv2.imread("screen.png", cv2.IMREAD_COLOR)

# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))

# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(
    gray_blurred,
    cv2.HOUGH_GRADIENT,
    1,
    20,
    param1=50,
    param2=30,
    minRadius=1,
    maxRadius=40,
)

# Draw circles that are detected.
if detected_circles is not None:

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)

        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
cv2.imshow("Detected Circle", img)
cv2.waitKey(0)
