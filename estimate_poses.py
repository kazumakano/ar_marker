import time
import cv2
import numpy as np
from cv2 import aruco
import script.utility as util


def estim_poses_from_img(cam_file: str, dict_idx: int, marker_len: float, file: str) -> None:
    pass

def estim_poses_from_vid(cam_file: str, dict_idx: int, marker_len: float, file: str) -> None:
    pass

def estim_poses_on_stream(cam_file: str, dict_idx: int, marker_len: float, uri: str) -> None:
    cam_mat, cam_dist_coef = util.load_cam_data(cam_file)
    cap = cv2.VideoCapture(filename=uri)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)

    print("press any key to exit")

    while True:
        ret, img = cap.read()
        if not ret:
            # reconnect
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(filename=uri)
            continue

        corners, ids = aruco.detectMarkers(img, prof_dict)[:2]

        util.draw_ids(corners, ids, img)
        util.draw_poses(cam_mat, cam_dist_coef, img, *aruco.estimatePoseSingleMarkers(corners, marker_len, cam_mat, cam_dist_coef)[:2])

        cv2.imshow("stream", img)

        key = cv2.waitKey(delay=1)
        if key != -1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cam_file", required=True, help="specify camera calibration file", metavar="PATH_TO_CAM_FILE")
    parser.add_argument("-l", "--len", type=float, required=True, help="specify marker length", metavar="LEN")
    parser.add_argument("-d", "--dict", default=aruco.DICT_APRILTAG_16h5, type=int, help="specify profile dictionary index", metavar="IDX")
    parser.add_argument("-i", "--img_file", help="specify image file", metavar="PATH_TO_IMG_FILE")
    parser.add_argument("-s", "--stream", help="specify video stream", metavar="URI")
    parser.add_argument("-v", "--vid_file", help="specify video file", metavar="PATH_TO_VID_FILE")
    args = parser.parse_args()

    if args.img_file is not None:
        estim_poses_from_img(args.dict, args.img_file)
    elif args.stream is not None:
        estim_poses_on_stream(args.cam_file, args.dict, args.len, args.stream)
    elif args.vid_file is not None:
        estim_poses_from_vid(args.dict, args.vid_file)
