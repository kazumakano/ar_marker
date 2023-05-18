import os.path as path
from os import mkdir
import cv2
import numpy as np
from cv2 import aruco


def create_markers(dict_idx: int, margin_ratio: float, num: int, resolution: int) -> None:
    dir_per_dict = path.normpath(path.join(path.dirname(__file__), "marker/", str(dict_idx)))
    if not path.exists(dir_per_dict):
        mkdir(dir_per_dict)

    pad_width = int(margin_ratio * resolution / 2)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)
    for i in range(num):
        cv2.imwrite(path.join(dir_per_dict, str(i) + ".png"), np.pad(aruco.drawMarker(prof_dict, i, resolution - 2 * pad_width), pad_width, constant_values=255))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", type=int, required=True, help="specify number of markers to create", metavar="NUM")
    parser.add_argument("-d", "--dict", default=aruco.DICT_APRILTAG_16h5, type=int, help="specify profile dictionary index", metavar="IDX")
    parser.add_argument("-m", "--margin", default=0, type=float, help="specify margin ratio", metavar="RATIO")
    parser.add_argument("-r", "--resolution", default=512, type=int, help="specify image resolution", metavar="RESOLUTION")
    args = parser.parse_args()

    create_markers(args.dict, args.margin, args.num, args.resolution)
