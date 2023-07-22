import os.path as path
import time
import cv2
from cv2 import aruco
import script.utility as util

FPS = 5

def detect_markers_from_img(dict_idx: int, file: str, export: bool = False) -> None:
    img = cv2.imread(file)

    corners, ids = aruco.detectMarkers(img, aruco.getPredefinedDictionary(dict_idx))[:2]
    print(f"{len(corners)} markers were detected")

    aruco.drawDetectedMarkers(img, corners)
    util.draw_ids(corners, ids, img)

    cv2.imshow("image", img)

    print("press any key to exit")
    cv2.waitKey()

    if export:
        cv2.imwrite(path.join(path.dirname(__file__), "result/", path.basename(file)), img)

    cv2.destroyAllWindows()

def detect_markers_from_vid(dict_idx: int, file: str, export: bool = False, start: float = 0) -> None:
    cap = cv2.VideoCapture(filename=file)
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000 * start)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)
    if export:
        recorder = cv2.VideoWriter(path.join(path.dirname(__file__), "result/", path.basename(file)), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    print("press any key to exit")

    while True:
        ret, img = cap.read()
        if not ret:
            break

        corners, ids = aruco.detectMarkers(img, prof_dict)[:2]

        aruco.drawDetectedMarkers(img, corners)
        util.draw_ids(corners, ids, img)

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

def detect_markers_on_stream(dict_idx: int, uri: str, export: bool = False) -> None:
    cap = cv2.VideoCapture(filename=uri)
    prof_dict = aruco.getPredefinedDictionary(dict_idx)
    if export:
        recorder = cv2.VideoWriter(path.join(path.dirname(__file__), "result/stream.mkv"), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    print("press any key to exit")

    while True:
        ret, img = cap.read()
        if not ret:
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(filename=uri)
            continue

        corners, ids = aruco.detectMarkers(img, prof_dict)[:2]

        aruco.drawDetectedMarkers(img, corners)
        util.draw_ids(corners, ids, img)

        cv2.imshow("stream", img)
        if export:
            recorder.write(img)

        key = cv2.waitKey(delay=1)
        if key != -1:
            break

    cap.release()
    if export:
        recorder.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dict", default=aruco.DICT_APRILTAG_16h5, type=int, help="specify profile dictionary", metavar="IDX")
    parser.add_argument("-e", "--export", action="store_true", help="export result")
    parser.add_argument("-i", "--img_file", help="specify image file", metavar="PATH_TO_IMG_FILE")
    parser.add_argument("-s", "--stream", help="specify video stream", metavar="URI")
    parser.add_argument("-v", "--vid_file", help="specify video file", metavar="PATH_TO_VID_FILE")
    parser.add_argument("--start", default=0, type=float, help="specify time to start video [s]", metavar="TIME")
    args = parser.parse_args()

    if args.img_file is not None:
        detect_markers_from_img(args.dict, args.img_file, args.export)
    elif args.stream is not None:
        detect_markers_on_stream(args.dict, args.stream, args.export)
    elif args.vid_file is not None:
        detect_markers_from_vid(args.dict, args.vid_file, args.export, args.start)
