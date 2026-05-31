import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import urllib.request
import os
import time


_LEFT_HIP       = 23
_RIGHT_HIP      = 24
_LEFT_KNEE      = 25
_RIGHT_KNEE     = 26
_LEFT_SHOULDER  = 11
_RIGHT_SHOULDER = 12
_NOSE           = 0

POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26),
    (25, 27), (26, 28),
]

MODEL_PATH = "pose_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
)


def _ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("[LunarGuard] Baixando modelo MediaPipe Pose (~3 MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


class FallDetector:
    def __init__(self):
        _ensure_model()

        base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.4,
            min_pose_presence_confidence=0.4,
            min_tracking_confidence=0.4,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        self.landmarks = None
        self._last_fall = False

    def process(self, frame_rgb) -> bool:
        ts = int(time.time() * 1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        result = self._landmarker.detect_for_video(mp_image, ts)

        if not result.pose_landmarks:
            self.landmarks = None
            return self._last_fall

        lm = result.pose_landmarks[0]
        self.landmarks = lm

        def y(idx):
            return lm[idx].y

        def vis(idx):
            return lm[idx].visibility

        avg_hip_vis = (vis(_LEFT_HIP) + vis(_RIGHT_HIP)) / 2

        avg_hip  = (y(_LEFT_HIP)      + y(_RIGHT_HIP))      / 2
        avg_knee = (y(_LEFT_KNEE)     + y(_RIGHT_KNEE))     / 2
        avg_sh   = (y(_LEFT_SHOULDER) + y(_RIGHT_SHOULDER)) / 2
        nose_y   = y(_NOSE)

        hip_below_knee = avg_hip >= avg_knee - 0.08
        shoulders_low  = abs(avg_sh - avg_hip) < 0.20
        fall_by_hips   = avg_hip_vis >= 0.3 and hip_below_knee and shoulders_low

        nose_sh_diff = abs(nose_y - avg_sh)
        fall_by_head = nose_sh_diff < 0.12

        self._last_fall = fall_by_hips or fall_by_head
        return self._last_fall

    def close(self):
        self._landmarker.close()
