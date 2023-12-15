import cv2
import base64
import requests
from flask import Flask, Response, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
api_key = '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'


def frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')


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
        self.template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)

    def detect_winner_with_openai(self, frame):
        base64_image = frame_to_base64(frame)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Each side represents a different player, player 1 and player 2. A winner is detected when the indicator lights on each light up. There are usually two dots that illuminate on the screen when one side wins. Splitting the screen down the middle, which side of the screen, (left or right) wins?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            return response.json()  # Interpret this based on your requirement
        except Exception as e:
            print(f"Error: {e}")
            return None


def gen_frames(processor, video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        winner_response = processor.detect_winner_with_openai(frame)
        # Interpret winner_response here to extract the winner information
        # ...

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
        "1": (0, 0, 422, 20),
        "2": (480, 0, 580, 20)
    }
    threshold = 0.80
    processor = ImageProcessor(template_path, detection_regions, threshold)

    return Response(gen_frames(processor, video_path), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/mk")
def winner():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_directory, "video", "T100vsScorpion.mp4")
    template_path = os.path.join(current_directory, "assets", "t100Dots.png")

    detection_regions = {
        "1": (0, 0, 422, 20),
        "2": (480, 0, 580, 20)
    }
    threshold = 0.70

    processor = ImageProcessor(template_path, detection_regions, threshold)

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        winner_response = processor.detect_winner_with_openai(frame)
        # Interpret winner_response here to extract the winner information
        # For example, analyze the response from the OpenAI API to determine the winner
        # This part of the code will depend on the response structure from OpenAI

        if winner_response:  # Assuming winner_response contains information about the winner
            # Extract winner information from winner_response
            # Update result accordingly
            result = {"winner": "Player 1 or Player 2 based on response"}
            break

    cap.release()
    cv2.destroyAllWindows()

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
