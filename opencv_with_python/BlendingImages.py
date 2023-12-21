import cv2 as cv

#blending of two images of different sizes

#Loading both the images
dino = cv.imread('./data/dino.webp')
house = cv.imread('./data/house.jpg')

#exdending the size of the image to look a big
dino=cv.resize(dino, (350, 550))

# picking the region of interest in the house image
#roi must be equall the size of the daino image
roi = house[50:650, 280:630]

#converting daino image color to gray from bgr
dino2gray = cv.cvtColor(dino, cv.COLOR_BGR2GRAY)

#removing the background and taking only the Dinosaur from the image
_,mask = cv.threshold(dino2gray,245,255,cv.THRESH_BINARY)

#taking inverse of the mask to black the background
mask_inv=cv.bitwise_not(mask)

#adding dino mask to the roi taken from the house image
roi_mask = cv.bitwise_and(roi, roi, mask=mask)

#adding imverse of the mask to the dino image
dino_mask = cv.bitwise_and(dino, dino, mask=mask_inv)

#adding both of the mask togather to restore their respective colors
final_roi=cv.add(roi_mask, dino_mask)

#adding the final roi to the indexes from where roi was taken in the house image
house[50:650,280:630] = final_roi

#showing the final image created
cv.imshow('final_image',house)

#waiting for a key to press to end the program
cv.waitKey(0)

