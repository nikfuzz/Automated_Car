#
# def keys_to_output(keys):
#     #(A,W,D]
#     output = [0,0,0]
#     if 'A' in keys:
#         output[0]=1
#     elif 'W' in keys:
#         output[1]=1
#     elif 'D' in keys:
#         output[2]=1
#     return output
import numpy as np
import cv2
import time
import pyautogui
from directkeys import PressKey, ReleaseKey, W, A, S, D
from draw_lanes import draw_lanes
from grabscreen import grab_screen


def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, 255)

    # returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

    vertices = np.array([[10, 469], [10, 281], [300, 188], [500, 188], [800, 281], [800, 469]], np.int32)

    processed_img = roi(processed_img, [vertices])

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho   theta   thresh  min length, max gap:
    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 20, 15)
    m1 = 0
    m2 = 0
    try:
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)


            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img, original_image, m1, m2


def straight():
    PressKey(W)
    time.sleep(0.04)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(W)

def left():
    # for i in range(10):
        PressKey(A)
        ReleaseKey(W)
        PressKey(W)
        time.sleep(0.04)
        ReleaseKey(D)
        ReleaseKey(A)


def right():
    # for i in range(1):
        PressKey(D)
        ReleaseKey(W)
        PressKey(W)
        time.sleep(0.04)
        ReleaseKey(A)
        ReleaseKey(D)


def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    PressKey(S)
    time.sleep(0.04)
    ReleaseKey(S)

for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

last_time = time.time()
while True:
    screen = grab_screen(region=(0, 40, 800, 600))
    print('Frame took {} seconds'.format(time.time() - last_time))
    last_time = time.time()
    new_screen, original_image, m1, m2 = process_img(screen)
    # cv2.imshow('window', new_screen)
    cv2.imshow('window2', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

    if m1 < 0 and m2 < 0:
        right()
    elif m1 > 0 and m2 > 0:
        left()
    elif (m1>0 and m2<0) or (m1<0 and m2>0) :
        straight()
    else:
        slow_ya_roll()

    # cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
