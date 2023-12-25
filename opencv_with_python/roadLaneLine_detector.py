import cv2 as cv
import numpy as np

""" This method mask everything other than the region of interest, It get the same colors 
as that of the image provided by in the region of interest"""


def roi(image, vertices):
    mask = np.zeros_like(image)
    mask_color = 255
    cv.fillPoly(mask, vertices, mask_color)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image


"""This method creates a blank image of the size of the original image and draw green lines
at their respective positions which are detected in the original image. At the end we add this 
blank image with lines to the original image"""


def draw_lines(image, lines):
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=5)
    image = cv.addWeighted(image, 0.9, blank_image, 1, 0.0)
    return image


"""This method defined the vertices for the area of interest where we want to draw the 
lines of the road lanes. secondly it converts the image to gray scal so that we can appy the 
Canny edge detector. lastly the probabilistic Hough lines transform is applied to detect
the lines which fulfil some criteria"""


def detect_lines(image):
    roi_vertices = [(200, 720), (605, 420), (700, 420), (1280, 720)]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    canny_img = cv.Canny(gray, 100, 200)
    cropped_img = roi(canny_img, np.array([roi_vertices], np.int32))
    lines = cv.HoughLinesP(cropped_img, rho=3, theta=np.pi / 180, threshold=180, lines=np.array([]),
                           minLineLength=40, maxLineGap=25)
    image_lines = draw_lines(image, lines)
    return image_lines


""""Here we load the video from the specified path and resize it because the 
size of the original video is very large"""
cap = cv.VideoCapture('./data/road.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.resize(frame, (1280, 720))
    output_image = detect_lines(frame)
    cv.imshow('output_image', output_image)
    if cv.waitKey(1) & 0xFF == ord('s'):
        break
cap.release()
cv.destroyAllWindows()