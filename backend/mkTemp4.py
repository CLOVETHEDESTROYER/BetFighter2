import cv2
import numpy as np
import os
import json
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class ImageProcessor:
    def __init__(self, template_path, detection_regions, threshold):
        self.template_path = template_path
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
        self.template = cv2.resize(template, dim, interpolation = cv2.INTER_AREA)
    
    def detect_winner(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for region_name, region_coords in self.detection_regions.items():
            region = gray[region_coords[1]:region_coords[3], region_coords[0]:region_coords[2]]
            res = cv2.matchTemplate(region, self.template, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(res)
            if max_val > self.threshold:
                return region_name
        return None

def gen_frames(processor, video_path):
    cap = cv2.VideoCapture(video_path)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        winner = processor.detect_winner(frame)
        if winner is not None:
            print(f"{winner} Side Wins")
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_directory, "video", "T100vsScorpion.mp4")
    template_path = os.path.join(current_directory, "assets", "t100Dots.png")

    detection_regions = {
        "player1 Won": (0, 0, 422, 20),
        "Player2 Won": (480, 0, 580, 20)
    }
    threshold = 0.80
    processor = ImageProcessor(template_path, detection_regions, threshold)

    return Response(gen_frames(processor, video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/mk")
def winner():
    # Define the detection regions for the left and right sides
    detection_regions = {
        "player1 Won": (0, 0, 422, 20),
        "Player2 Won": (480, 0, 580, 20)
    }
    
    # Set the threshold value for detecting the template image
    threshold = 0.70

    # Set up the video capture object
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_directory, "video", "T100vsScorpion.mp4")
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Print the size of the frame
    print(f'Frame size: {width} x {height}')
    
    # Initialize the image processor
    current_directory = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_directory, "assets", "t100Dots.png")
    processor = ImageProcessor(template_path, detection_regions, threshold)

    # Initialize result variable with a default value
    result = {"winner": "No Winner"}

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        #flips the image.  Using as a test.
        frame = cv2.flip(frame, 1)

        # If the frame was not grabbed, break
        if not ret:
            break

        # Detect the winner
        winner = processor.detect_winner(frame)
        if winner is not None:
            print(f"{winner.capitalize()} Side Wins")
            result = {"winner": winner}
            

            # Encode the resulting frame as JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = img_encoded.tobytes()
            data = json.dumps(result)
            cap.release()
            cv2.destroyAllWindows()
            return Response(response=data, status=200, content_type='image/jpeg')
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True, port=8000)

