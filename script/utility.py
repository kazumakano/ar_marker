import cv2
import numpy as np
from cv2 import aruco


def draw_detected_markers(corners: tuple[np.ndarray, ...], ids: np.ndarray, img: np.ndarray) -> None:
    aruco.drawDetectedMarkers(img, corners)
    for i in range(len(corners)):
        cv2.putText(img, str(ids[i, 0]), (int(corners[i][0, :, 0].mean()), int(corners[i][0, :, 1].min()) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)
