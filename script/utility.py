import cv2
import numpy as np
import yaml


def draw_ids(corners: tuple[np.ndarray, ...], ids: np.ndarray, img: np.ndarray) -> None:
    for i in range(len(corners)):
        cv2.putText(img, str(ids[i, 0]), (int(corners[i][0, :, 0].mean()), int(corners[i][0, :, 1].min()) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)

def draw_poses(cam_mat: np.ndarray, cam_dist_coef: np.ndarray, img: np.ndarray, marker_len: float, rvecs: np.ndarray | None, tvecs: np.ndarray | None) -> None:
    if rvecs is not None and tvecs is not None:
        for i in range(len(rvecs)):
            cv2.drawFrameAxes(img, cam_mat, cam_dist_coef, rvecs[i], tvecs[i], marker_len)

def load_cam_data(file: str) -> tuple[np.ndarray, np.ndarray]:
    with open(file) as f:
        data = yaml.safe_load(f)

    return np.array(data["camera_matrix"]["data"], dtype=np.float32).reshape(3, 3), np.array(data["distortion_coefficients"]["data"], dtype=np.float32)
