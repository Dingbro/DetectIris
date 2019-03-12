import argparse
import os
import numpy as np
import cv2 as cv


def detect_iris(image_path, output_path, dp, param1, param2, minRadius=300, maxRadius=150):
    image = cv.imread(image_path)
    output = image.copy()
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    circles_out = cv.HoughCircles(image=image_gray,
                                  method=cv.HOUGH_GRADIENT,
                                  dp=dp,
                                  minDist=10000,
                                  param1=param1,
                                  param2=param2,
                                  minRadius=minRadius)

    circles_in = cv.HoughCircles(image=image_gray,
                                 method=cv.HOUGH_GRADIENT,
                                 dp=dp,
                                 minDist=10000,
                                 param1=param1,
                                 param2=param2,
                                 maxRadius=maxRadius)

    flag_out = True
    flag_in = True

    # print(circles_out, circles_in)

    if circles_out is not None:
        circles_out = np.round(circles_out[0, :]).astype("int")
        for (x, y, r) in circles_out:
            cv.circle(output, (x, y), r, (0, 255, 0), 4)
            cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    else:
        flag_out = False

    if circles_in is not None:
        circles_in = np.round(circles_in[0, :]).astype("int")
        for (x, y, r) in circles_in:
            cv.circle(output, (x, y), r, (0, 255, 0), 4)
            cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    else:
        flag_in = False

    if (not flag_out) and (not flag_in):
        print("Neither circle was detected")
        return
    if not flag_out:
        print("Only inner circle was detected")
        return
    if not flag_in:
        print("only outer circle was detected")
        return

    image_name = image_path[image_path.index('/')+1:]
    image_name = image_name[:image_name.index('.')]
    if output_path is None:
        if not os.path.isdir('./results/{}'.format(image_name)):
            os.mkdir('./results/{}'.format(image_name))
        cv.imwrite("results/{}/{}_dp={}_p1={}_p2={}_mr={}_Mr={}.png".format(image_name,
                                                                            image_name,
                                                                            dp,
                                                                            param1,
                                                                            param2,
                                                                            minRadius,
                                                                            maxRadius),
                   np.hstack([image, output]))
    else:
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        cv.imwrite("{}/{}_dp={}_p1={}_p2={}_mr={}_Mr={}.png".format(output_path,
                                                                    image_name,
                                                                    dp,
                                                                    param1,
                                                                    param2,
                                                                    minRadius,
                                                                    maxRadius),
                   np.hstack([image, output]))



#2, 8, 22 = x, y, 1280
#iris127.bmp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    ap.add_argument("-dp", "--invratio", default=1.2, type=float, help="The inverse ratio of resolution\nSamller it is,"
                                                                       " more accurate detection, but more likely to "
                                                                       "miss slightly degenerated circles.")
    #ap.add_argument("-md", "--mindist", default=10000, type=int,
                    #help="The minimum distance between two detected circles")
    ap.add_argument("-p1", "--param1", default=200, type=int,
                    help="Upper threshold for the internal Canny edge detector")
    ap.add_argument("-p2", "--param2", default=100, type=int, help="Threshold for center detection. "
                                                                   "Increase it to avoid false detections.")
    ap.add_argument("-mr", "--minRadius", default=300, type=int, help="Minimum radius of outer circle")
    ap.add_argument("-Mr", "--maxRadius", default=150, type=int, help="Maximum radius of inner circle")
    args = vars(ap.parse_args())

    detect_iris(args['image'], args['invratio'], args['param1'], args['param2'], args['minRadius'], args['maxRadius'])

