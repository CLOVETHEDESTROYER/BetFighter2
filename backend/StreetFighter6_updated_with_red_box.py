
import cv2
import numpy as np
import os
import json
from flask import Flask, Response, jsonify

app = Flask(__name__)


class ImageProcessor:
    def __init__(self, template_path, threshold):
        self.template_path = template_path
        self.threshold = threshold
        self.template = None
        self.load_template()

    def load_template(self):
        try:
            self.template = cv2.imread(
                self.template_path, cv2.IMREAD_GRAYSCALE)
            if self.template is None:
                raise ValueError(
                    f"Could not read template image at {self.template_path}")
        except Exception as e:
            print(f"Exception while reading the template: {e}")
            raise

    def detect_winner(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        right_region = gray[:, :int(frame.shape[1]/2)]
        left_region = gray[:, int(frame.shape[1]/2):]
        regions = {'Left': left_region, 'Right': right_region}

        for region_name, region in regions.items():
            res = cv2.matchTemplate(
                region, self.template, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(res)
            if max_val > self.threshold:
                return region_name
        return None


@app.route('/video_feed')
def video_feed():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(
        current_directory, "video", "Streetfighter6test.mp4")
    template_path = os.path.join(current_directory, "assets", "WON.png")
    threshold = 0.6884

    processor = ImageProcessor(template_path, threshold)

    def gen_frames():
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            # frame = cv2.flip(frame, 1)  # Add this line to flip the frame

            if not ret:
                break

            # Draw a green line down the center
            center_x = int(frame.shape[1] / 2)
            cv2.line(frame, (center_x, 0), (center_x,
                     frame.shape[0]), (0, 255, 0), 2)

            winner = processor.detect_winner(frame)
            if winner:
                print(f"{winner} Side Wins")
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()
        cv2.destroyAllWindows()

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/mk")
def winner():
    frame = None  # Initialize frame to avoid UnboundLocalError
    threshold = 0.68

    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(
        current_directory, "video", "Streetfighter6test.mp4")
    template_path = os.path.join(current_directory, "assets", "WON.png")

    processor = ImageProcessor(template_path, threshold)
    result = {"winner": "No Winner"}

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        winner = processor.detect_winner(frame)
        if winner:
            print(f"{winner} Side Wins")
            result = {"winner": winner}
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = img_encoded.tobytes()
            data = json.dumps(result)
            cap.release()
            cv2.destroyAllWindows()
            return jsonify(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
