import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
def nothing(val):
    pass

img = cv.imread('./data/butterfly.jpg', cv.IMREAD_GRAYSCALE)

title_window = 'Canny'
cv.namedWindow(title_window)
cv.createTrackbar('Threshold1', title_window, 0, 255, nothing)
cv.createTrackbar('Threshold2', title_window, 0, 255, nothing)
cv.setTrackbarPos('Threshold2',title_window, 255,)

while(1):

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    th1 = cv.getTrackbarPos('Threshold1', title_window)
    th2 = cv.getTrackbarPos('Threshold2', title_window)
    canny = cv.Canny(img, th1, th2)
    cv.imshow(title_window, canny)
    cv.imwrite('butterfly_output.jpg',canny)
cv.destroyWindow()