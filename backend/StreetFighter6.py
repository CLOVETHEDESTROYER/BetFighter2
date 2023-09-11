# Combining the code from mkTemp3.py and StreetFighter6.py

# Importing required libraries
import cv2
import numpy as np
import pyautogui
import os
from flask import Flask, Response

app = Flask(__name__)

# ImageProcessor class from mkTemp3.py


class ImageProcessor:
    def __init__(self, detection_regions, threshold):
        self.template_path = os.path.join("WONSF6.png")
        self.detection_regions = detection_regions
        self.threshold = threshold
        self.template = None
        self.load_template()

    def load_template(self):
        template = cv2.imread(self.template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise ValueError("Could not read template image")
        scale_percent = 60
        width = int(template.shape[1] * scale_percent / 100)
        height = int(template.shape[0] * scale_percent / 100)
        dim = (width, height)
        self.template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)

    def detect_winner(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for region_name, region_coords in self.detection_regions.items():
            region = gray[region_coords[1]:region_coords[3],
                          region_coords[0]:region_coords[2]]
            res = cv2.matchTemplate(
                region, self.template, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(res)
            if max_val > self.threshold:
                return region_name
        return None

# Endpoint for capturing screen and detecting specific image


@app.route('/detect_image')
def detect_image():
    # Capture the content of the primary monitor
    screenshot_image = pyautogui.screenshot()
    frame = np.array(screenshot_image)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Split the screen into two halves (Left and Right)
    height, width, _ = frame.shape
    left_region = (0, 0, width // 2, height)
    right_region = (width // 2, 0, width, height)

    # Define detection regions
    detection_regions = {
        "Left": left_region,
        "Right": right_region
    }
    threshold = 0.80
    processor = ImageProcessor(detection_regions, threshold)

    # Detect the winner (Left or Right)
    winner = processor.detect_winner(frame)
    if winner is not None:
        print(f"{winner} Side Detected")

    # Encode the frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    response = buffer.tobytes()
    return Response(response, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)
