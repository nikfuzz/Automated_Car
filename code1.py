import numpy as np
import cv2
import time
from PIL import ImageGrab

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 255)
    return processed_img

last_time = time.time()
while(1):
    screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
    new_screen = process_img(screen)

    print('Loop took {} seconds'. format(time.time() - last_time))
    last_time = time.time()

    cv2.imshow('window',new_screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
