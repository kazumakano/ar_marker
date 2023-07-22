import os.path as path
import time
import cv2
from cv2 import aruco
import script.utility as util

FPS = 5

def estim_poses_from_img(cam_file: str, dict_idx: int, marker_len: float, img_file: str) -> None:
    pass

def estim_poses_from_vid(cam_file: str, dict_idx: int, marker_len: float, vid_file: str, export: bool = False, start: float = 0) -> None:
    cam_mat, cam_dist_coef = util.load_cam_data(cam_file)
    cap = cv2.VideoCapture(filename=vid_file)
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000 * start)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)
    if export:
        recorder = cv2.VideoWriter(path.join(path.dirname(__file__), "result/", path.splitext(path.basename(vid_file))[0] + "_pose.mkv"), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    print("press any key to exit")

    while True:
        ret, img = cap.read()
        if not ret:
            break

        corners, ids = aruco.detectMarkers(img, prof_dict)[:2]

        util.draw_ids(corners, ids, img)
        util.draw_poses(cam_mat, cam_dist_coef, img, marker_len, *aruco.estimatePoseSingleMarkers(corners, marker_len, cam_mat, cam_dist_coef)[:2])

        cv2.imshow("video", img)
        if export:
            recorder.write(img)

        key = cv2.waitKey(delay=1)
        if key != -1:
            break

    cap.release()
    if export:
        recorder.release()
    cv2.destroyAllWindows()

def estim_poses_on_stream(cam_file: str, dict_idx: int, marker_len: float, uri: str) -> None:
    cam_mat, cam_dist_coef = util.load_cam_data(cam_file)
    cap = cv2.VideoCapture(filename=uri)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)

    print("press any key to exit")

    while True:
        ret, img = cap.read()
        if not ret:
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(filename=uri)
            continue

        corners, ids = aruco.detectMarkers(img, prof_dict)[:2]

        util.draw_ids(corners, ids, img)
        util.draw_poses(cam_mat, cam_dist_coef, img, marker_len, *aruco.estimatePoseSingleMarkers(corners, marker_len, cam_mat, cam_dist_coef)[:2])

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
    parser.add_argument("-d", "--dict", default=aruco.DICT_APRILTAG_16h5, type=int, help="specify profile dictionary", metavar="IDX")
    parser.add_argument("-e", "--export", action="store_true", help="export result")
    parser.add_argument("-i", "--img_file", help="specify image file", metavar="PATH_TO_IMG_FILE")
    parser.add_argument("-s", "--stream", help="specify video stream", metavar="URI")
    parser.add_argument("-v", "--vid_file", help="specify video file", metavar="PATH_TO_VID_FILE")
    parser.add_argument("--start", default=0, type=float, help="specify time to start video", metavar="TIME")
    args = parser.parse_args()

    if args.img_file is not None:
        estim_poses_from_img(args.dict, args.img_file)
    elif args.stream is not None:
        estim_poses_on_stream(args.cam_file, args.dict, args.len, args.stream)
    elif args.vid_file is not None:
        estim_poses_from_vid(args.cam_file, args.dict, args.len, args.vid_file, args.export, args.start)
