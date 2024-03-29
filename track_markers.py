import csv
import os.path as path
import cv2
from cv2 import aruco
import script.utility as util


def track_markers_from_vid(cam_file: str, dict_idx: int, marker_len: float, vid_file: str, start: float = 0) -> None:
    cam_mat, cam_dist_coef = util.load_cam_data(cam_file)
    cap = cv2.VideoCapture(filename=vid_file)
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000 * start)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)

    with open(path.join(path.dirname(__file__), "result/", path.splitext(path.basename(vid_file))[0] + ".csv"), mode="w", newline="") as f:
        print("press any key to exit")

        writer = csv.writer(f)
        while True:
            ret, img = cap.read()
            if not ret:
                break

            corners, ids = aruco.detectMarkers(img, prof_dict)[:2]
            rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, marker_len, cam_mat, cam_dist_coef)[:2]

            util.draw_ids(corners, ids, img)
            util.draw_poses(cam_mat, cam_dist_coef, img, marker_len, rvecs, tvecs)

            cv2.imshow("video", img)

            if ids is not None:
                for i, id in enumerate(ids):
                    writer.writerow((cap.get(cv2.CAP_PROP_POS_FRAMES), id[0], *tvecs[i][0], *rvecs[i][0]))

            if cv2.waitKey(delay=1) != -1:
                break

    cap.release()
    cv2.destroyAllWindows()

def track_markers_on_stream(cam_file: str, dict_idx: int, marker_len: float, uri: str) -> None:
    pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cam_file", required=True, help="specify camera calibration file", metavar="PATH_TO_CAM_FILE")
    parser.add_argument("-l", "--len", type=float, required=True, help="specify marker length", metavar="LEN")
    parser.add_argument("-d", "--dict", default=aruco.DICT_APRILTAG_16h5, type=int, help="specify profile dictionary", metavar="IDX")
    parser.add_argument("-s", "--stream", help="specify video stream", metavar="URI")
    parser.add_argument("-v", "--vid_file", help="specify video file", metavar="PATH_TO_VID_FILE")
    parser.add_argument("--start", default=0, type=float, help="specify time to start video", metavar="TIME")
    args = parser.parse_args()

    if args.stream is not None:
        track_markers_on_stream(args.cam_file, args.dict, args.len, args.stream)
    elif args.vid_file is not None:
        track_markers_from_vid(args.cam_file, args.dict, args.len, args.vid_file, args.start)
