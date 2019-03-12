import argparse
import numpy as np
from detect_circle import detect_iris


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-ir", "--imageRange", nargs="+", type=int, default=[100, 101],
                    help="First and last image index to be searched.")
    ap.add_argument("-dpr", "--invratioRange", nargs="+", type=float, default=[1, 1],
                    help="Minimum and maximum value of the inverse ratio range."
                         "Will be divided with step of 0.1")
    ap.add_argument("-p1r", "--param1Range", nargs="+", default=[200, 200], type=int,
                    help="Minimum and maximum value of param1."
                         "Will be divided with step of 10.")
    ap.add_argument("-p2r", "--param2Range", nargs="+", default=[100, 100], type=int,
                    help="Minimum and maximum value of param2. "
                         "Will be divided with step of 10")
    ap.add_argument("-o", "--outputPath", type=str, default=None,
                    help="Path to the folder that output images will be stored."
                         "By default, output images will be saved in ./results/[original_image_name].")
    args = vars(ap.parse_args())

    output_path = args["outputPath"]
    for image_index in range(args["imageRange"][0], args["imageRange"][1]+1):
        image_path = "images/iris{}.bmp".format(image_index)
        print("Start analyzing image iris{}.bmp".format(image_index))
        for dp in np.arange(args["invratioRange"][0], args["invratioRange"][1]+0.1, 0.1):
            for p1 in range(args["param1Range"][0], args["param1Range"][1]+10, 10):
                for p2 in range(args["param2Range"][0], args["param2Range"][1]+10, 10):
                    print(image_path, dp, p1, p2)
                    detect_iris(image_path, output_path, dp, p1, p2)
