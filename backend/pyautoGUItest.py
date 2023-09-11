import cv2
import numpy as np
import pyautogui

# Load the template image
template = cv2.imread('/backend/assets/dots.png', cv2.IMREAD_UNCHANGED)
if template.shape[-1] == 4:
    # Remove alpha channel
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
else:
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Get a screenshot of the screen
screen = np.array(pyautogui.screenshot())
screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

# Perform template matching
result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)

# Get the location of the best match
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
match_location = max_loc

# Draw a rectangle around the match on the screenshot
template_height, template_width = template.shape[:2]
cv2.rectangle(screen, match_location, (match_location[0] + template_width, match_location[1] + template_height), (0, 255, 0), 2)

# Display the result
cv2.imshow('Result', screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
