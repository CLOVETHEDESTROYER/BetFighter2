import cv2
import numpy as np
import os
import json
from flask import Flask


# Load the image you want to detect

try:
    template = cv2.imread('backend/assets/dots.png', cv2.IMREAD_GRAYSCALE)
    w, h = template.shape

except:
    AttributeError

# template = cv2.resize(img,(20, 50), fx=1, fy=1)
# Resize image and template

scale_percent = 62  # percent of original size
width = int(template.shape[1] * scale_percent / 100)
height = int(template.shape[0] * scale_percent / 100)
dim = (width, height)
template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)


# Set up the video capture object
cap = cv2.VideoCapture('backend/video/T100vsScorpion.mov', 0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # toggle the below code to test image on both sides of fram
    # frame = cv2.flip(frame, 1)

    # If the frame was not grabbed, break
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Define the two detection regions
    left = gray[25:58, 725:795]
    right = gray[25:58, 920:990]
    # left = gray[0:20, 100:422]
    # right = gray[0:20, 480:580]

    # Detect the image in each region
    result1 = cv2.matchTemplate(left, template, cv2.TM_CCORR_NORMED)
    result2 = cv2.matchTemplate(right, template, cv2.TM_CCORR_NORMED)
    # result1 = cv2.matchTemplate(frame[25:322, 0:422], img, cv2.TM_CCORR_NORMED)
    # result2 = cv2.matchTemplate(frame[25:480, 0:580], img, cv2.TM_CCORR_NORMED)

    # Find the maximum value in each region
    _, max_val1, _, _ = cv2.minMaxLoc(result1)
    _, max_val2, _, _ = cv2.minMaxLoc(result2)
    print(max_val1, max_val2)

    # If the image was detected in region 1, draw a rectangle around it
    if max_val1 > .96:
        cv2.rectangle(frame, (100, 150), (800, 0), (0, 0, 255), 7)
    # If the image was detected in region 2, draw a rectangle around it
    if max_val2 > .925:
        cv2.rectangle(frame, (1600, 150), (880, 0), (255, 0, 0), 7)

    winner = {}
    # If the image was detected in region 1, return "Left Side Wins"
    if max_val1 > .96:
        winner['winner'] = left
        print("LEFT SIDE WINS")
    # If the image was detected in region 2, return "Region 2"
    elif max_val2 > .925:
        winner['winner'] = right
        print("RIGHT SIDE WINS")
    # If the image was not detected in either region, return "Not found"
    else:
        winner['winner'] = "Not found"
        print("NOT FOUND")

    # Return the winner output as a JSON response

    # Display the resulting frame
    # def Winner():
    # Your code to check for thresholds and find the winner here
    #    winner = (if max_val1 > .89: "LEFT SIDE WINS" elif max_val2 > .89: "RIGHT SIDE WINS" else: "Not found")
    # Return the winner output as a JSON response
    #    return json.dumps({'winner': winner})

    # Show the frame
    cv2.imshow('Frame', frame)
    cv2.imshow('ROI', left)
    cv2.imshow('ROI2', right)
    cv2.imshow('Template', template)

    # Check for user input
    if cv2.waitKey(1) == ord('q'):
        break


def Winner(left, right):
    img = cv2.imread('backend/assets/dots12.jpg', cv2.IMREAD_GRAYSCALE)
    template = cv2.imread('backend/assets/dots12.jpg', cv2.IMREAD_GRAYSCALE)
    # w, h = template.shape

    # Perform template matching
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # Get the maximum correlation coefficient and its position
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Create a dictionary to store the winner information
    winner = {}

    # If the image was detected in region 1, set the winner to "Left Side Wins"
    if max_val > 0.89:
        winner['winner'] = left
    # If the image was detected in region 2, set the winner to "Right Side Wins"
    else:
        winner['winner'] = right

    # Add the maximum correlation coefficient to the dictionary
    winner['correlation_coefficient'] = max_val

    # Return the dictionary as a JSON object
    return winner


cap.release()
cv2.destroyAllWindows()
