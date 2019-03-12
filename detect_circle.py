import argparse
import numpy as np
import cv2 as cv


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
output = image.copy()
image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

circles = cv.HoughCircles(image=image_gray,
                          method=cv.HOUGH_GRADIENT,
                          dp=1.2,
                          minDist=1000)
                          #param1=,
                          #param2=,
                          #minRadius=80,
                          #maxRadius=150)

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        cv.circle(output, (x, y), r, (0, 255, 0), 4)
        cv.rectangle(output, (x-5, y-5), (x+5, y+5), (0, 128, 255), -1)

    cv.imwrite("results/output.png", np.hstack([image, output]))
else:
    print("No circle detected.")

#2, 8, 22 = x, y, 1280
#iris127.bmp
