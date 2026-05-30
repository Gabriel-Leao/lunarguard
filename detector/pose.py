import mediapipe as mp
import numpy as np


class FallDetector:
    """
    Usa MediaPipe Pose para detectar quedas/colapso.
    Critério: quadril abaixo dos joelhos E ombros próximos do quadril
    (pessoa deitada ou colapsada no chão).
    """

    def __init__(self):
        self._mp_pose = mp.solutions.pose
        self._pose = self._mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,          # mais leve, suficiente para tempo real
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.landmarks = None

    def process(self, frame_rgb) -> bool:
        """
        Processa frame RGB e retorna True se uma queda for detectada.
        Também armazena landmarks para o overlay desenhar o esqueleto.
        """
        results = self._pose.process(frame_rgb)
        self.landmarks = results.pose_landmarks

        if not results.pose_landmarks:
            return False

        lm = results.pose_landmarks.landmark
        mp_pose = self._mp_pose.PoseLandmark

        def y(idx):
            return lm[idx].y  # normalizado 0-1 (maior = mais abaixo na tela)

        left_hip   = y(mp_pose.LEFT_HIP)
        right_hip  = y(mp_pose.RIGHT_HIP)
        left_knee  = y(mp_pose.LEFT_KNEE)
        right_knee = y(mp_pose.RIGHT_KNEE)
        left_sh    = y(mp_pose.LEFT_SHOULDER)
        right_sh   = y(mp_pose.RIGHT_SHOULDER)

        avg_hip    = (left_hip + right_hip) / 2
        avg_knee   = (left_knee + right_knee) / 2
        avg_sh     = (left_sh + right_sh) / 2

        # Queda: quadril abaixo ou no nível dos joelhos
        # E ombros próximos do quadril (diferença < 15% da altura normalizada)
        hip_below_knee = avg_hip >= avg_knee - 0.05
        shoulders_low  = abs(avg_sh - avg_hip) < 0.15

        return hip_below_knee and shoulders_low

    def close(self):
        self._pose.close()
