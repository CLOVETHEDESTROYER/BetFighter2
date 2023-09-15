import pyautogui
import cv2


image = cv2.imread('/backend/assets/dots.png')
if image is None:
    print("Image could not be opened.")
else:
    print("Image successfully opened.")
