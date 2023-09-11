import cv2
import numpy as np
import os
import json

# Load the template image
current_directory = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_directory, "assets", "dots.png")
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
print(f"Template file path: {template_path}")
print(f"Template read status: {template is not None}")

# Resize image and template
scale_percent = 60 # percent of original size
width = int(template.shape[1] * scale_percent / 100)
height = int(template.shape[0] * scale_percent / 100)
dim = (width, height)
template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)

# Define the detection region variables
left_region = (725, 25, 795, 59)
right_region = (920, 25, 990, 58)

# Define the threshold value for detecting the template image
threshold = 0.80

# Set up the video capture object
current_directory = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(current_directory, "video", "T100vsScorpion.mp4")
cap = cv2.VideoCapture(video_path)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Video file path: {video_path}")


# Print the size of the frame
print(f'Frame size: {width} x {height}')

def draw_rectangle(frame, region, color):
    x, y, w, h = region
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 7)

def Winner():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cv2.flip(frame, 1)

        # If the frame was not grabbed, break
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the template image in the left and right regions
        left = gray[left_region[1]:left_region[3], left_region[0]:left_region[2]]
        right = gray[right_region[1]:right_region[3], right_region[0]:right_region[2]]
        res_left = cv2.matchTemplate(left, template, cv2.TM_CCOEFF_NORMED)
        res_right = cv2.matchTemplate(right, template, cv2.TM_CCOEFF_NORMED)

        # Find the maximum correlation coefficient in each region
        max_val_left = np.max(res_left)
        max_val_right = np.max(res_right)

        # Draw a rectangle around the detected template image
        if max_val_left > threshold:
            draw_rectangle(frame, left_region, (0, 0, 255))
            print("Left Side Wins")
            result = {"winner": "left"}
            cap.release()
            cv2.destroyAllWindows()
            return json.dumps(result)
        elif max_val_right > threshold:
            draw_rectangle(frame, right_region, (0, 0, 255))
            print("Right Side Wins")
            result = {"winner": "right"}
            cap.release()
            cv2.destroyAllWindows()
            return json.dumps(result)

        cv2.imshow('frame', frame)
        cv2.imshow('left', left)
        cv2.imshow('right', right)
        cv2.imshow('dots', template)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    response = {"winner": "No Winner"}
    return json.dumps(result)

if __name__ == "__main__":
    print(Winner())

       
