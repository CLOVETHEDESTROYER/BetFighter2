import cv2
import numpy as np
import os
import json
from flask import Flask

# Load the image you want to detect
template = cv2.imread('backend/assets/dots12.jpg', cv2.IMREAD_GRAYSCALE)
#w, h = template.shape[::-1]
#template = cv2.resize(img,(20, 50), fx=1, fy=1)

def Winner():
    img = cv2.imread('backend/assets/dots12.jpg',0)
    template = cv2.imread('backend/assets/dot12.jpg',0)
    w, h = template.shape[::-1]
    print (img)

    # print template shape for debugging
    print(f"template shape: {template.shape}")

    # Perform template matching
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # print max_val for debugging
    print(f"max_val: {max_val}")

    # check if max_val is greater than 0.89
    if max_val > 0.89:
        return True
    else:
        return False


cap = cv2.VideoCapture('backend/video/T100vsScorpion.mp4', 0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Print the size of the frame
print(f'Frame size: {width} x {height}')

while (cap.isOpened()):
    # Capture frame-by-frame
     # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            assert not isinstance(frame,type(None)), 'frame not found'

    


    # Convert the frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Define the two detection regions 
    #left = gray[420:frame.shape[1]//2, 0:frame.shape[2]//40]
    #right = gray[430:frame.shape[1]//2, frame.shape[1]//2:frame.shape[1]]
    #left = gray[(25, 0), (322, 422)]
    #right = gray[(25, 0), (480, 580)]
    #left = gray[(25, 250), (2, 90)]
    #right = gray[(275, 450), (2, 90)]
    #left = gray[25:0, 322:422]
    #right = gray[25:0, 480:580]
left = gray[0:20, 100:422]
right = gray[0:20, 480:580]
    

    # Detect the image in each region
result1 = cv2.matchTemplate(left, template, cv2.TM_CCORR_NORMED)
result2 = cv2.matchTemplate(right, template, cv2.TM_CCORR_NORMED)
    #result1 = cv2.matchTemplate(frame[25:322, 0:422], img, cv2.TM_CCORR_NORMED)
    #result2 = cv2.matchTemplate(frame[25:480, 0:580], img, cv2.TM_CCORR_NORMED)


    # Find the maximum value in each region
_, max_val1, _, _ = cv2.minMaxLoc(result1)
_, max_val2, _, _ = cv2.minMaxLoc(result2)
print(max_val1, max_val2)


    # If the image was detected in region 1, draw a rectangle around it
if max_val1 > .94068063:
        cv2.rectangle(frame, (322, 25), (422, 0), (0, 0, 255), 7)
    # If the image was detected in region 2, draw a rectangle around it
if max_val2 > .82:
        cv2.rectangle(frame, (480, 25), (580, 0), (255, 0, 0), 7)


    # If the image was detected in region 1, return "Left Side Wins"
if max_val1 > .89: 
        print ("LEFT SIDE WINS")  
    # If the image was detected in region 2, return "Region 2"
elif max_val2 > .89: 
        print ("RIGHT SIDE WINS") 
    # If the image was not detected in either region, return "Not found"
else: 
        print ("NOT FOUND")
        

    # Display the resulting frame
    #def Winner():
    # Your code to check for thresholds and find the winner here
    #    winner = (if max_val1 > .89: "LEFT SIDE WINS" elif max_val2 > .89: "RIGHT SIDE WINS" else: "Not found")
    # Return the winner output as a JSON response
    #    return json.dumps({'winner': winner})
    

    # these boxes are to calibrate the screen over the "victory dots" Uncomment to calibrate
    #imgOGL = cv2.rectangle(frame, (420, frame.shape[1]//2), (0,frame.shape[2]//40), (255, 0, 255), 2)
    #imgOGR = cv2.rectangle(frame, (430, frame.shape[1]//2), (frame.shape[1]//1,frame.shape[1]//4), (255, 255, 255), 4)
    #imgT = cv2.rectangle(frame, (25, frame.shape[2]//4), (422, frame.shape[0]//4), (0, 255, 0), 5)
    #imgTR = cv2.rectangle(frame, (480, frame.shape[0]//4), (902,frame.shape[2]), (0, 0, 220), 5)

imgL = cv2.rectangle(frame, (322, 25), (422, 0), (255, 0, 0), 5)
imgR = cv2.rectangle(frame, (480, 25), (580, 0), (255, 255, 0), 5)




   

    # Show the frame
cv2.imshow('Frame', frame)
cv2.imshow('ROI', right)


        

    # Check for user input
if cv2.waitKey(1) == ord('q'):
             

    cap.release()
cv2.destroyAllWindows()

